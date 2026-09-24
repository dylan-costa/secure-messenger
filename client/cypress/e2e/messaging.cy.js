// End-to-end check that mirrors the manual verification done during
// development: two real users, a real RSA handshake, a real message sent
// and decrypted in an actual browser -- not a mock. Requires both the
// backend (port 8000) and `npm run dev` (port 5173) to be running.

const runId = Date.now()
const userA = `cypressA_${runId}`
const userB = `cypressB_${runId}`
const password = "pw12345"
const messageText = "Hello from Cypress!"

function signUp(username) {
  cy.contains("Sign up").click()
  cy.get('input[placeholder="Username"]').type(username)
  cy.get('input[placeholder="Password"]').type(password)
  cy.contains("button", "Sign up").click()
  cy.contains(`Logged in as: ${username}`)
}

function logOut() {
  cy.contains("Logout").click()
}

function logIn(username) {
  cy.get('input[placeholder="Username"]').type(username)
  cy.get('input[placeholder="Password"]').type(password)
  cy.contains("button", "Login").click()
  cy.contains(`Logged in as: ${username}`)
}

describe("secure messaging, end to end", () => {
  it("lets two real users establish an RSA conversation and exchange a decrypted message", () => {
    cy.visit("/")
    signUp(userA)
    logOut()

    cy.visit("/")
    signUp(userB)
    logOut()

    // Alice starts the conversation and picks the method. Since Bob hasn't
    // opened it yet, his identity key doesn't exist server-side, so the app
    // correctly puts Alice into a "waiting for peer" state here -- there is
    // no message box to type into yet, on purpose.
    cy.visit("/")
    logIn(userA)
    cy.contains(userB).click()
    cy.contains("button", "RSA").click()
    cy.contains("Waiting for", { timeout: 10000 })
    logOut()

    // Bob opening the conversation is what completes the handshake: it
    // generates his RSA key, uploads it, and finds Alice's key already
    // waiting -- so his view goes straight to "ready" and he can send.
    cy.visit("/")
    logIn(userB)
    cy.contains(userA).click()
    cy.get('input[placeholder="Type a message..."]', { timeout: 10000 }).type(messageText)
    cy.contains("button", "Send").click()

    // Bob should see his OWN sent message decrypted correctly -- this
    // specifically exercises the ciphertext_for_sender self-copy path.
    cy.contains(messageText)
    logOut()

    // Alice reopens the conversation: her earlier "waiting" poll (or a
    // fresh visit, as here) now finds Bob's key and decrypts the same
    // message independently, with her own private key.
    cy.visit("/")
    logIn(userA)
    cy.contains(userB).click()
    cy.contains(messageText, { timeout: 10000 })
  })
})
