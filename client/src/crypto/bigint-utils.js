// Shared BigInt helpers for the RSA-family crypto module. JS BigInt has no
// builtin modPow/modInverse/primality test, so these mirror what
// pycryptodome/Python's 3-arg pow() do internally in server/encryption/rsa.py.

export function modPow(base, exponent, modulus) {
    if (modulus === 1n) return 0n

    let result = 1n
    let b = base % modulus
    let e = exponent

    while (e > 0n) {
        if (e & 1n) {
            result = (result * b) % modulus
        }
        e >>= 1n
        b = (b * b) % modulus
    }

    return result
}

// Extended Euclidean algorithm, used for modular inverse (JS has no
// equivalent of Python's `pow(e, -1, mod)`).
export function modInverse(a, modulus) {
    let [oldR, r] = [a % modulus, modulus]
    let [oldS, s] = [1n, 0n]

    while (r !== 0n) {
        const quotient = oldR / r
        ;[oldR, r] = [r, oldR - quotient * r]
        ;[oldS, s] = [s, oldS - quotient * s]
    }

    if (oldR !== 1n) {
        throw new Error("Modular inverse does not exist")
    }

    return ((oldS % modulus) + modulus) % modulus
}

function randomBigInt(bits) {
    const byteLength = Math.ceil(bits / 8)
    const bytes = new Uint8Array(byteLength)
    crypto.getRandomValues(bytes)

    // Force the top bit so the candidate is always exactly `bits` bits long.
    bytes[0] |= 0x80

    let value = 0n
    for (const byte of bytes) {
        value = (value << 8n) | BigInt(byte)
    }

    return value
}

const SMALL_PRIMES = [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n, 41n, 43n, 47n]

function isProbablePrime(n, rounds = 20) {
    if (n < 2n) return false

    for (const p of SMALL_PRIMES) {
        if (n === p) return true
        if (n % p === 0n) return false
    }

    // Miller-Rabin: write n-1 as 2^r * d with d odd.
    let d = n - 1n
    let r = 0n
    while (d % 2n === 0n) {
        d /= 2n
        r += 1n
    }

    witnessLoop: for (let i = 0; i < rounds; i++) {
        const a = 2n + (randomBigInt(64) % (n - 3n))
        let x = modPow(a, d, n)

        if (x === 1n || x === n - 1n) continue

        for (let j = 0n; j < r - 1n; j++) {
            x = modPow(x, 2n, n)
            if (x === n - 1n) continue witnessLoop
        }

        return false
    }

    return true
}

export function gcd(a, b) {
    while (b !== 0n) {
        ;[a, b] = [b, a % b]
    }
    return a
}

export function generatePrime(bits) {
    while (true) {
        let candidate = randomBigInt(bits)
        candidate |= 1n // force odd

        if (isProbablePrime(candidate)) {
            return candidate
        }
    }
}
