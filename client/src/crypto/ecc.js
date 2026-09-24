// Port of server/encryption/ecc.py's ECC/Diffie-Hellman logic (point
// arithmetic, key generation, shared-secret derivation, XOR cipher). Uses
// plain Number arithmetic -- the field prime is always <10000 by design (a
// toy curve, generated server-side once per conversation), so nothing here
// approaches Number.MAX_SAFE_INTEGER. The point-at-infinity search for a
// generator point is NOT ported -- that stays server-side, reusing the
// existing (non-secret, public-parameter) Python ECCurve class.

function mod(a, m) {
    return ((a % m) + m) % m
}

function modInverse(a, m) {
    let [oldR, r] = [mod(a, m), m]
    let [oldS, s] = [1, 0]

    while (r !== 0) {
        const quotient = Math.floor(oldR / r)
        ;[oldR, r] = [r, oldR - quotient * r]
        ;[oldS, s] = [s, oldS - quotient * s]
    }

    if (oldR !== 1) {
        throw new Error("Modular inverse does not exist")
    }

    return mod(oldS, m)
}

// A point is either {x, y} or null (the point at infinity).

export function pointDouble(point, a, p) {
    if (point === null) return null
    if (mod(point.y, p) === 0) return null

    const lambda = mod((3 * point.x * point.x + a) * modInverse(2 * point.y, p), p)
    const x3 = mod(lambda * lambda - 2 * point.x, p)
    const y3 = mod(lambda * (point.x - x3) - point.y, p)

    return { x: x3, y: y3 }
}

export function pointAdd(p1, p2, a, p) {
    if (p1 === null) return p2
    if (p2 === null) return p1

    if (p1.x === p2.x) {
        if (mod(p1.y + p2.y, p) === 0) {
            return null // p2 == -p1
        }
        return pointDouble(p1, a, p)
    }

    const lambda = mod((p2.y - p1.y) * modInverse(p2.x - p1.x, p), p)
    const x3 = mod(lambda * lambda - p1.x - p2.x, p)
    const y3 = mod(lambda * (p1.x - x3) - p1.y, p)

    return { x: x3, y: y3 }
}

export function scalarMult(point, scalar, a, p) {
    let result = null
    let addend = point
    let k = scalar

    while (k > 0) {
        if (k & 1) {
            result = pointAdd(result, addend, a, p)
        }
        addend = pointDouble(addend, a, p)
        k >>= 1
    }

    return result
}

function randomScalar(p) {
    const range = p - 1 // private key in [1, p-1]
    const bytes = new Uint32Array(1)
    crypto.getRandomValues(bytes)

    return (bytes[0] % range) + 1
}

export function generateKeys(domainParams) {
    const { p, a, gx, gy } = domainParams
    const G = { x: gx, y: gy }

    const privateKey = randomScalar(p)
    const publicKey = scalarMult(G, privateKey, a, p)

    return { privateKey, publicKey }
}

export function generateSharedSecret(privateKey, otherPublicKey, domainParams) {
    const { p, a } = domainParams
    const sharedPoint = scalarMult(otherPublicKey, privateKey, a, p)
    return mod(sharedPoint.x, 256)
}

export function encrypt(message, sharedSecret) {
    const bytes = new TextEncoder().encode(message)
    let hex = ""
    for (const byte of bytes) {
        hex += (byte ^ sharedSecret).toString(16).padStart(2, "0")
    }
    return hex
}

export function decrypt(ciphertextHex, sharedSecret) {
    const byteCount = ciphertextHex.length / 2
    const bytes = new Uint8Array(byteCount)

    for (let i = 0; i < byteCount; i++) {
        const byte = parseInt(ciphertextHex.slice(i * 2, i * 2 + 2), 16)
        bytes[i] = byte ^ sharedSecret
    }

    return new TextDecoder().decode(bytes)
}

export function serializePublicKey(publicKey) {
    return JSON.stringify({ x: publicKey.x, y: publicKey.y })
}

export function deserializePublicKey(json) {
    return JSON.parse(json)
}
