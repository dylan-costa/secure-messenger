import { describe, it, expect } from "vitest"
import { modPow, modInverse, generatePrime, gcd } from "./bigint-utils.js"

describe("modPow", () => {
    it("computes modular exponentiation correctly", () => {
        expect(modPow(4n, 13n, 497n)).toBe(445n)
    })
})

describe("modInverse", () => {
    it("finds a value that multiplies back to 1 mod m", () => {
        const a = 17n
        const m = 3120n
        const inverse = modInverse(a, m)
        expect((a * inverse) % m).toBe(1n)
    })

    it("throws when no inverse exists", () => {
        expect(() => modInverse(6n, 9n)).toThrow()
    })
})

describe("gcd", () => {
    it("computes the greatest common divisor", () => {
        expect(gcd(48n, 18n)).toBe(6n)
        expect(gcd(17n, 5n)).toBe(1n)
    })
})

describe("generatePrime", () => {
    it("returns an odd number of exactly the requested bit length", () => {
        const p = generatePrime(64)
        expect(p % 2n).toBe(1n)
        expect(p.toString(2).length).toBe(64)
    })

    it("is not divisible by small primes (sanity check, not a full primality proof)", () => {
        const p = generatePrime(64)
        for (const small of [3n, 5n, 7n, 11n, 13n]) {
            expect(p % small).not.toBe(0n)
        }
    })
})
