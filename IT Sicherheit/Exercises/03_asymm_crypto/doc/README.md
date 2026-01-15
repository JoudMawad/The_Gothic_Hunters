# Attacks on Asymmetric-Key Cryptography

## 1. Alice wants to trick Bob into signing a message m. She knows that Bob is using plain RSA. Alice prepares two messages $m_1$, $m_2$ ∈ Z such that $m_1$ · $m_2 \pmod{N} = m$, and asks Bob to sign $m_1$ and $m_2$ using his private key d, which Bob does.

### a) (2 points) How does the attack continue and why does it work?
Since RSA has the multiplicative property:
$$
(m_1 \cdot m_2)^d \equiv m_1^d \cdot m_2^d \pmod{N}
$$

So if Bob signs $m_1$ and $m_2$ this means Alice would have $s_1$ and $s_2$:

- $s_1 = m_1^d \pmod{N}$
- $s_2 = m_2^d \pmod{N}$

Since $m \equiv m_1 \cdot m_2 \pmod{N}$, alice can now compute the signature for $m$:

$$
m^d\pmod{N} \equiv (m_1 m_2)^d \pmod{N}
       \equiv (m_1^d \cdot m_2^d) \pmod{N}
       \equiv s_1 \cdot s_2 \pmod{N}
$$

Therefore, Alice has the signature for $m$ without Bob signing $m$, only because he signed $m_1$ and $m_2$:

$$
s = s_1 \cdot s_2 \pmod{N}
$$

This $s$ is a valid RSA signature on $m$, even though Bob never signed $m$.

### b) (5 points) Master: Bob has decided to use a publicly known hash function H to prevent Alice from forging signatures. Instead of signing a message m directly Bob from now on will sign H(m). Explain how this approach prevents forgeries. Name 3 required properties the function H should have to prevent forgeries in general.
#### How this approach prevents forgeries? ####

If bob uses a hash function $H$ the signature becomes: $s = H(m)^d (mod N)$.

Since $H(m) \neq H(m_1) \cdot H(m_2)$, Alice can no longer compute $H(m) = H(m_1) \cdot H(m_2) \mod (N)$

So the multiplicative property is no longer there.

#### 3 required properties the function H should have to prevent forgeries in general:
1. For a specific m, it must be computationally infeasible to find another message $m^′$ and $m \neq m^′$ such that satisfies: $H(m) = H(m^′)$
2. Given a hash value $y$, it must be computationally infeasible to find any message $m$ such that: $H(m) = y$
3. There should be a strong collision resistance: It must be computationally infeasible to find any two different messages $m_1\neq m_2$ such that: $H(m_1) = H(m_2)$

## 2. Alice writes a lover letter to Bob. She signs the letter then encrypts it with Bob’s public key and sends it to Bob. Unfortunately, Bob plays false. He decrypts the letter and encrypts it with Dave’s public key. He then forwards the letter to Dave, such that Dave believes Alice loves him. This is called surreptitious forwarding.
### (a) (2 points) Does first encrypting and then signing the message solve Alices problem? Is there another problem?
#### Does first encrypting and then signing the message solve Alices problem?
Yes it solves Alices problem, because if Alice signs the message after encryption and sends it to Bob, Bob would have Alices signature on the ciphertext $c$ that is made using his public key $k$ and if he tried to change the ciphertext $c$ for Davids public key $k^′$, then Alices signature won't be valid for the new ciphertext $c^′$.
#### Is there another problem?
Yes there is, it is loss of deniability, since Alice signed the ciphertext then it is tied to alice. Anyone who sees (c,s) can verfy that Alice signed this specific encrypted message, this remove Alice's deniability.
So while surreptitious forwarding is prevented, Alice's privacy is reduced.
### (b) (2 points) Describe a solution to improve both the sign-then-encrypt and encrypt-then-sign approach.
A good solution would be signing and encrypting in one step and then unsigning and decrypting in one step which is already a known method called Signcryption introduced by Zheng in 1997.
In this way we prevent the surreptitious forwarding because the user cannot extract a reusable signature and ensure deniability because only the intended reciever can verify the sender.

# Weird Service 

## 3.c
I succeeded because the authentication protocol is symmetric. Since the server authenticates the client in the exact same way the client authenticates the server, i can use a second connection to the server. By relaying the question or the "challenge" received in the first connection to the second one, the server solved its own challenge using what it has stored. i captured this valid response and sent it back to the first connection and i didnt even had to know what was the question of the server. 