import { describe, it, expect } from "vitest"
import * as ecc from "./ecc.js"

// Real domain params captured from a live server-generated ECCurve (not
// invented), so the "on curve" check below is meaningful.
const domainParams = { p: 2129, a: 144, b: 408, gx: 1007, gy: 888 }

function isOnCurve({ x, y }, { p, a, b }) {
    const lhs = (y * y) % p
    const rhs = (((x ** 3) + a * x + b) % p + p) % p
    return lhs === rhs
}

describe("ecc", () => {
    it("the test fixture's domain params are actually on the curve", () => {
        expect(isOnCurve({ x: domainParams.gx, y: domainParams.gy }, domainParams)).toBe(true)
    })

    it("two independently generated keypairs derive the same shared secret", () => {
        const alice = ecc.generateKeys(domainParams)
        const bob = ecc.generateKeys(domainParams)

        const aliceSecret = ecc.generateSharedSecret(alice.privateKey, bob.publicKey, domainParams)
        const bobSecret = ecc.generateSharedSecret(bob.privateKey, alice.publicKey, domainParams)

        expect(aliceSecret).toBe(bobSecret)
    })

    it("encrypts and decrypts a message with the shared secret", () => {
        const alice = ecc.generateKeys(domainParams)
        const bob = ecc.generateKeys(domainParams)
        const sharedSecret = ecc.generateSharedSecret(alice.privateKey, bob.publicKey, domainParams)
        const message = "hey bob, this is alice"

        const ciphertext = ecc.encrypt(message, sharedSecret)

        expect(ecc.decrypt(ciphertext, sharedSecret)).toBe(message)
    })

    it("pointDouble(G) matches pointAdd(G, G)", () => {
        const G = { x: domainParams.gx, y: domainParams.gy }

        const doubled = ecc.pointDouble(G, domainParams.a, domainParams.p)
        const added = ecc.pointAdd(G, G, domainParams.a, domainParams.p)

        expect(doubled).toEqual(added)
    })

    it("a point plus its negation is the point at infinity", () => {
        const G = { x: domainParams.gx, y: domainParams.gy }
        const negG = { x: G.x, y: (domainParams.p - G.y) % domainParams.p }

        expect(ecc.pointAdd(G, negG, domainParams.a, domainParams.p)).toBeNull()
    })

    it("adding the point at infinity is the identity operation", () => {
        const G = { x: domainParams.gx, y: domainParams.gy }

        expect(ecc.pointAdd(null, G, domainParams.a, domainParams.p)).toEqual(G)
    })

    it("scalarMult(G, 2) matches pointDouble(G)", () => {
        const G = { x: domainParams.gx, y: domainParams.gy }

        const doubled = ecc.pointDouble(G, domainParams.a, domainParams.p)
        const viaScalar = ecc.scalarMult(G, 2, domainParams.a, domainParams.p)

        expect(viaScalar).toEqual(doubled)
    })

    it("serializes and deserializes a public key", () => {
        const alice = ecc.generateKeys(domainParams)

        const restored = ecc.deserializePublicKey(ecc.serializePublicKey(alice.publicKey))

        expect(restored).toEqual(alice.publicKey)
    })
})
