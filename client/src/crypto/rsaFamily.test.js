import { describe, it, expect } from "vitest"
import * as rsaFamily from "./rsaFamily.js"

describe("rsaFamily", () => {
    it("encrypts and decrypts a message correctly (2-prime RSA)", () => {
        const { publicKey, privateKey } = rsaFamily.generateKeys(2, 256)
        const message = "Hello Bob, this is Alice!"

        const ciphertext = rsaFamily.encrypt(message, publicKey)

        expect(rsaFamily.decrypt(ciphertext, privateKey)).toBe(message)
    })

    it("encrypts and decrypts a message correctly (3-prime Multiprime RSA)", () => {
        const { publicKey, privateKey } = rsaFamily.generateKeys(3, 128)
        const message = "multiprime test 123"

        const ciphertext = rsaFamily.encrypt(message, publicKey)

        expect(rsaFamily.decrypt(ciphertext, privateKey)).toBe(message)
    })

    it("produces a different modulus for independently generated keys", () => {
        const a = rsaFamily.generateKeys(2, 256)
        const b = rsaFamily.generateKeys(2, 256)

        expect(a.publicKey.n).not.toBe(b.publicKey.n)
    })

    it.each(["a", "A", "0", " ", "!!!", "The quick brown fox 42."])(
        "round-trips messageToInteger/integerToMessage for %j",
        (message) => {
            const asInt = rsaFamily.messageToInteger(message)
            expect(rsaFamily.integerToMessage(asInt)).toBe(message)
        }
    )

    it("rejects a message longer than the key's modulus can hold", () => {
        const { publicKey } = rsaFamily.generateKeys(2, 256)
        const max = rsaFamily.maxMessageLength(publicKey.n)

        expect(() => rsaFamily.encrypt("x".repeat(max + 50), publicKey)).toThrow()
    })

    it("serializes and deserializes a public key", () => {
        const { publicKey } = rsaFamily.generateKeys(2, 256)

        const restored = rsaFamily.deserializePublicKey(rsaFamily.serializePublicKey(publicKey))

        expect(restored).toEqual(publicKey)
    })

    it("serializes and deserializes a private key", () => {
        const { privateKey } = rsaFamily.generateKeys(2, 256)

        const restored = rsaFamily.deserializePrivateKey(rsaFamily.serializePrivateKey(privateKey))

        expect(restored).toEqual(privateKey)
    })
})
