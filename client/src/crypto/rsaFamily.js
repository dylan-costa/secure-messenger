// Generalized port of server/encryption/rsa.py: standard RSA and Multiprime
// RSA are the same algorithm parameterized by prime count. n = p1*p2*...*pr,
// phi(n) = product(pi - 1), same C = M^e mod n / M = C^d mod n as the
// original Python. Runs entirely client-side -- private keys never leave
// the browser.

import { modPow, modInverse, generatePrime, gcd } from "./bigint-utils.js"

// Generate `primeCount` DISTINCT primes of `bitsPerPrime` bits each.
function generateDistinctPrimes(primeCount, bitsPerPrime) {
    const primes = []

    while (primes.length < primeCount) {
        const candidate = generatePrime(bitsPerPrime)
        if (!primes.includes(candidate)) {
            primes.push(candidate)
        }
    }

    return primes
}

export function generateKeys(primeCount, bitsPerPrime) {
    const primes = generateDistinctPrimes(primeCount, bitsPerPrime)

    let n = 1n
    let totient = 1n
    for (const p of primes) {
        n *= p
        totient *= (p - 1n)
    }

    let e = 65537n
    while (gcd(e, totient) !== 1n) {
        e += 2n
    }

    const d = modInverse(e, totient)

    return {
        publicKey: { e, n },
        privateKey: { d, n },
    }
}

// Mirrors rsa.py's message_to_integer: each character's full Unicode
// codepoint, zero-padded to 3 decimal digits, concatenated into one integer.
// Iterate by codepoint (not UTF-16 code unit) to match Python's ord().
export function messageToInteger(message) {
    let digits = ""
    for (const char of message) {
        digits += String(char.codePointAt(0)).padStart(3, "0")
    }
    return BigInt(digits)
}

// Mirrors integer_to_message: pad the decimal string up to the next
// multiple of 3 (recovers any leading zero digits int() parsing lost),
// then chunk into groups of 3 and turn each back into a character.
export function integerToMessage(messageNumber) {
    let digits = messageNumber.toString()

    if (digits.length % 3 !== 0) {
        const targetLength = (Math.floor(digits.length / 3) + 1) * 3
        digits = digits.padStart(targetLength, "0")
    }

    let message = ""
    for (let i = 0; i < digits.length; i += 3) {
        const codepoint = Number(digits.slice(i, i + 3))
        message += String.fromCodePoint(codepoint)
    }

    return message
}

export function encrypt(message, publicKey) {
    const { e, n } = publicKey
    const M = messageToInteger(message)

    if (M >= n) {
        throw new Error("Message is too large for this key.")
    }

    const C = modPow(M, e, n)
    return C.toString()
}

export function decrypt(ciphertext, privateKey) {
    const { d, n } = privateKey
    const C = BigInt(ciphertext)
    const M = modPow(C, d, n)
    return integerToMessage(M)
}

// How many characters can safely fit under a given modulus `n`, given the
// 3-decimal-digits-per-character packing above.
export function maxMessageLength(n) {
    const digitCount = n.toString().length
    return Math.max(0, Math.floor((digitCount - 1) / 3))
}

export function serializePublicKey(publicKey) {
    return JSON.stringify({ e: publicKey.e.toString(), n: publicKey.n.toString() })
}

export function deserializePublicKey(json) {
    const parsed = JSON.parse(json)
    return { e: BigInt(parsed.e), n: BigInt(parsed.n) }
}

export function serializePrivateKey(privateKey) {
    return JSON.stringify({ d: privateKey.d.toString(), n: privateKey.n.toString() })
}

export function deserializePrivateKey(json) {
    const parsed = JSON.parse(json)
    return { d: BigInt(parsed.d), n: BigInt(parsed.n) }
}
