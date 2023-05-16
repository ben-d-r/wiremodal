---
Date: 2022-01-09 21:30
Tags: bitcoin
Status: 
Slug: /satoshi-dreams
---

# Satoshi Dreams of Electronic Cash

_I wrote this piece in spring 2021 when I was first exploring Bitcoin. It's structured as a reading guide for the Bitcoin whitepaper; as I dug into Nakamoto's work, I found I was Googling terms every few sentences. I made notes on what I read, which later became this guide._

The Bitcoin whitepaper was published to the metzdowd.com Cryptography Mailing List on October 31, 2008. Its pseudonymous author, Satoshi Nakamoto, [wrote](https://satoshi.nakamotoinstitute.org/emails/cryptography/1/):

_"I've been working on a new electronic cash system that's fully peer-to-peer, with no trusted third party._

_The main properties:_

-   _Double-spending is prevented with a peer-to-peer network._
-   _No mint or other trusted parties._
-   _Participants can be anonymous._
-   _New coins are made from Hashcash style proof-of-work._
-   _The proof-of-work for new coin generation also powers the network to prevent double-spending."_

[Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf) is now iconic in the cryptocurrency community, but its existence, much less its contents, is barely known to most people.

This is not necessarily surprising. Revolutionary scientific discoveries are rarely known by the paper in which they were first published. However, if you are interested in learning about how Bitcoin works, the whitepaper is the best place to start. It introduces the core critical concepts: digital signatures, cryptographic hash functions, and proof of work. It also describes the reason for its creation, a mission that has changed a bit through the years.

I'll begin by covering the primary background concepts that need to be understood before tackling the whitepaper. I will then attempt to summarize the key points of the whitepaper in plain language. By the end, you should hopefully understand how Satoshi achieved the main goals of Bitcoin.

## Background concepts

### Digital signatures

We've all had to produce a physical signature on some sort of legal document. When you think about it closely though, these are very insecure. A good calligrapher could pretty easily learn to forge someone's signature in a couple of hours. An individual will have slightly different signatures on a given day. Yet we rely on these physical marks to prove that a unique person made an agreement with someone else. A better way to sign an agreement is with a digital signature. A digital signature actually "looks" different for each agreement but in doing so it is far more secure.

Using a [cryptographic key generation algorithm](https://en.wikipedia.org/wiki/Public-key_cryptography), a signer is given a private key and a public key. The private key is known only to them; the public key is made available to anyone who needs to verify the signature. The signer then passes their private key and the message to be signed into a signing algorithm which outputs the digital signature. The digital signature may then be authenticated by anyone who has the public key by passing the message, the digital signature, and the public key into a signature verifying algorithm.

Crucially, the digital signature looks different for each message that is signed, and a digital signature for a given message can't be guessed without knowing the private key. The only way to forge a digital signature is to guess the private key; the probability of doing so is astronomically small.

Let's say you wanted to keep a ledger of financial transactions among friends. Bob owes Joe $100. If Bob doesn't sign this ledger entry, there's nothing stopping Joe from copying the transaction record a few times and suddenly Bob owes Joe $300, according to the ledger. Instead, in this toy digital ledger, Bob will sign a message that says "Transaction 1: Bob owes Joe $100" with his private key. Joe can verify this message using Bob's public key, the digital signature, and a signature verifying algorithm. The digital signature is recorded on the ledger. If Joe tries to copy it a few times, it's immediately obvious that he's done so because an identical digital signature will appear multiple times on the ledger and everyone with Bob's public key can see that this is "Transaction 1".

### Cryptographic hash functions

A cryptographic hash function is a mathematical algorithm that takes a data message of any size and outputs a string of bits of a fixed size, called a "hash" or a "digest". Hash functions work one way; you can use a message to generate a hash, but you can't use a hash to generate the message. This is one of its most critical features.

Hash functions have some more key features that are relevant to Bitcoin:

-   The same message will generate the same hash value every time it is calculated. This means it's easy to verify a hash value for a given message.
-   A small change to the message results in an uncorrelated hash value. In the example below, the digests are all the same size but the alphanumeric string is completely different with no discernible pattern.
-   It's extremely difficult, if not impossible, to find two messages with the same hash value.

![](https://img.wiremodal.net/images/Cryptographic_Hash_Function.png)

User:Jorge Stolfi based on Image:Hash_function.svg by Helix84, Public domain, via Wikimedia Commons

A hash function may be thought of as a digital fingerprint. No two messages share a hash value. In this way, it's useful for proof of knowledge. If I write a text file with some information, generate the hash value, and share it publicly (e.g. Twitter), I have effectively timestamped encrypted information. If I ever need to prove that I was in possession of this information, I can share the text file and anyone can verify that the hash matches that which was previously published. Satoshi Nakamoto famously timestamped the first Bitcoin block ("genesis block") with a headline from _The Times_ of London. This demonstrates that the block was mined no earlier than January 3, 2009.

![Raw hex version of the Bitcoin genesis block. Bitcoin Wiki. "Genesis block". CC BY 3.0](https://img.wiremodal.net/images/bitcoin_genesis.png)

03/Jan/2009 Chancellor on brink of second bailout for banks

### Proof-of-work

Cryptographic hash functions also form the basis of "proof-of-work", the system that maintains the security of the Bitcoin ledger. If we know that changing a small part of the message results in an uncorrelated hash output, and that hash functions don't work backward, we can then estimate how long it would take to generate a hash value that meets a predefined criterion.

Say we want a message that has a hash that starts with six zeros. There's a very small chance that you get this right away. For example, the message "Hello, world!" (UTF-8) gives the following SHA-256 hash:

`315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3`

No zeros at the beginning. So I try again, adding a number to the end. "Hello, world!1" gives the following hash:

`e9afc424b79e4f6ab42d99c81156d3a17228d6e1eef4139be78e948a9332a7d8`

Still no zeros. So I keep incrementing that number, called a nonce, running the SHA-256 algorithm over and over again until some version of that message gives me a hash that starts with six zeros. On average, I'll need to run the algorithm 16,777,216 times to find this hash (there are 16 possible characters for each position in the hash, so this is calculated as 16^6). In other words, I need to do a lot of computational work before finding a valid message. We'll learn how this computational proof-of-work secures the decentralized Bitcoin ledger when we dig into the whitepaper.

## Bitcoin: A Peer-to-Peer Electronic Cash System

We've explored the basic cryptographic principles that underpin the Bitcoin protocol. We're now ready to look at the Bitcoin whitepaper. Here, I'll provide a summary of each section, with some commentary where applicable. The entire paper is only eight pages; I encourage you to read it yourself.

### 1. Introduction

Internet commerce relies on trusted third parties to process payments. Satoshi Nakamoto sees a few inherent weaknesses in this system due to its reliance on centralized trust.

Completely non-reversible transactions aren't possible on the internet. Since all transactions go through some institution they can't avoid dispute mediation, whether as a customer service or due to legal requirements.

Mediation has a cost, and this limits the minimum practical transaction size. Micropayments are not feasible on the Visa network, for example, due to the transaction fees. There's also a hidden cost in the inability to make non-reversible payments for non-reversible services. If I eat a meal at a restaurant and pay on my credit card, I can chargeback that transaction but the restaurant can't ask me to regurgitate my lunch. The merchant must protect themselves in the case of this dispute, thus the cost of a meal is marginally higher than it would be if there were a completely non-reversible payment mechanism, assuming most people pay with a credit card instead of cash.

This asymmetry means that merchants require more customer data to protect themselves in case of fraud. Customers in turn must trust the merchant and the payment processor to handle their personal data securely. This can all be avoided by paying with physical cash, but there is not yet a means to make cash payments over a communications channel without a trusted intermediary.

This situation calls for an electronic payment system based on cryptographic proof instead of trust which would allow for two parties to transact without the need for a trusted intermediary. The proposed Bitcoin protocol demonstrates a solution for the double-spending problem by timestamping transactions for proof of chronological order. The system is secure so long as the honest nodes have more computational power than any group of attacker nodes.

### 2. Transactions

An electronic coin is a chain of digital signatures. To transfer a coin to another user, the owner digitally signs a hash of the previous transaction and the public key of the recipient and adds that data to the end of the coin. The recipient can verify each of the signatures on the chain to see the ownership history.

The main problem when implementing this system with an electronic coin is that the new owner cannot verify that a previous owner did not double-spend the coin. Theoretically, the owner could generate an unlimited number of copies of the chain of signatures and try to spend each (at a different location for each, to avoid being caught). Counterfeiting data on a computer is far easier than counterfeiting paper bills or metal coins. The default solution to this problem is to introduce a trusted intermediary that maintains a ledger of all coins and checks every transaction against this ledger of record. This solution is not ideal for the reasons previously discussed.

To construct a decentralized, peer-to-peer payment confirmation system, all participants need to be aware of all previous transactions. This means that all transactions must be announced to the entire network. Each node (computer) in the network must maintain a ledger and they must all agree on the contents of the ledger. The recipient of the electronic coin needs proof that the majority of the nodes agree that it was the first transaction received, thus not previously spent.

### 3. Timestamp server

Transactions must be timestamped so that the network knows the chronological order in which they were broadcast. This is achieved by collecting transactions in blocks of predetermined size and generating a hash of those data along with the hash of the previous block. The blocks are effectively chained together by including the hash of the previous block. There's no way to edit a past block without recalculating the hashes of it and all of the downstream blocks.

Transactions that are proposed for a new block are checked against the transactions that have been recorded in previous blocks. Identical transactions that appear in earlier blocks are rejected from the new block. This method solves the double-spending problem.

![](https://img.wiremodal.net/images/timestamp-server.svg)

[Bitcoin: A Peer-to-Peer Electronic Cash System](https://nakamotoinstitute.org/bitcoin/). Nakamoto Institute. [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

While the double-spending problem is solved, based on this description it appears to be trivial to edit the blockchain, especially in the case where you're trying to edit a recent block. Say the blockchain is 5 blocks long and you want to make a change to Block 3. You include the hash of Block 2, all the transactions of Block 3 (with the modified transaction), find that hash, and carry on with Blocks 4 and 5. If you can convince the majority of the nodes that this is the real blockchain you have successfully committed your fraud. After all, a SHA-256 hash can be calculated very quickly, just a few milliseconds on a modern computer. This is where proof-of-work comes in.

### 4. Proof-of-work

Satoshi based his proof-of-work system on Adam Back's [Hashcash](https://nakamotoinstitute.org/static/docs/hashcash.pdf). Each block also contains a nonce that is incremented to find a hash with a certain number of leading zero bits. This establishes a certain amount of work that must be completed before finding a valid hash for the block. In order to edit a previous block, you must redo all the work to find a hash with the requisite number of zero bits and do the same for all the downstream blocks. This turns a task that might take milliseconds to do once into a job that takes approximately 10 minutes.

![](https://img.wiremodal.net/images/proof-of-work.svg)

[Bitcoin: A Peer-to-Peer Electronic Cash System](https://nakamotoinstitute.org/bitcoin/). Nakamoto Institute. [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This proof-of-work system also solves the problem of obtaining majority consensus on the peer-to-peer network by forcing one-CPU-one-vote. The majority is represented by the longest chain which necessarily has the most work invested in it. If most of the computing power on the network is controlled by honest nodes, the honest chain will always grow faster than any fraudulent side chains.

### 5. Network

Satoshi outlined the following steps to run the peer-to-peer network (direct quote):

-   New transactions are broadcast to all nodes.
-   Each node collects new transactions into a block.
-   Each node works on finding a difficult proof-of-work for its block.
-   When a node finds a proof-of-work, it broadcasts the block to all nodes.
-   Nodes accept the block only if all transactions in it are valid and not already spent.
-   Nodes express their acceptance of the block by working on creating the next block in the chain, using the hash of the accepted block as the previous hash.

The protocol defines the correct chain to be the longest one, and all nodes will work to extend it. If two nodes broadcast a new block simultaneously, all other nodes will begin working from the block that they receive first. However, the other branch will be saved in case it becomes longer. This state will last only until the next block is announced on one of the two chains, at which point the nodes discard the shorter one and begin working on the longest chain.

The network is tolerant of dropped messages such as new transactions and new blocks. As long as most nodes receive a new transaction, it will eventually be incorporated into a new block. If a node does not receive notice of a new block it will realize that it's missing one when the next block is announced.

### 6. Incentive

The first transaction in a block is special in that it creates a new coin that is owned by the creator of the block. This block reward acts as an incentive for nodes to support the network and is a means to distribute coins into circulation. Nodes that expend computation time and electricity to find new blocks are often called "miners" because they are analogous to gold miners who expend resources to search for gold. This was not specified in the whitepaper, but the original block reward was 50 bitcoins. The protocol halves the block reward periodically after a predetermined number of blocks are mined (approximately every four years). Today, the block reward is 6.25 BTC.

Users may also incentivize block miners by leaving a transaction fee. Eventually, the only incentive will be transaction fees once a predetermined number of coins have been created. Satoshi doesn't mention this in the whitepaper, but the supply limit for bitcoin is 21 million coins.

The incentives encourage honesty among the nodes. If an individual or group manages to control more than half of the computational power on the network they must choose whether to defraud the network by overwriting their prior spend transactions or simply continuing to run the network as normal and collecting all of the block rewards. Satoshi expects that it is more profitable to do the latter; the attacker will amass more coins and will not undermine the system and therefore the validity of their wealth.

### 7. Reclaiming disk space

Satoshi designed the system in such a way that the transaction data can be discarded after enough time has passed to save space on a user's computer. This is done by basing the block hashes on a Merkle Tree, where only the root hash of the tree is included in the block header. This procedure is not critical to understanding how Bitcoin works, but the gist is that it makes it easier for any network user to confirm that a payment has been settled by the network without running a full node (a complete copy of the blockchain which comprises hundreds of gigabytes of data).

### 8. Payment verification

Payments can be verified by any network user by using the "pruned" Merkle Tree version of the blockchain, as described in the above section. The actual transaction data can't be checked (since it's been pruned off), but by finding the Merkle branch in which the transaction was timestamped the user can confirm that the network accepted it as long as it's somewhere in the longest blockchain.

As always, this verification method is only as secure as the network; if attackers control the majority of the computing power, they can fool other users who are using this verification method. It's safer to verify using a full node because then you would be able to see the fraudulent transaction data. Satoshi recommends that if a business is settling large values on the Bitcoin network that they run a full node for better verification.

### 9. Combining and splitting value

Each bitcoin can be divided into 100 million "cents" (these are now known as "satoshis" or sats). It would be unwieldy to process each satoshi as a separate transaction. Sending one bitcoin would mean processing 100 million transactions. Instead, a transaction combines one or multiple inputs and up to two outputs.

For example, say I own three addresses on the network: Address 1 holds 1 BTC, Address 2 holds 0.4 BTC, and Address 3 holds 0.8 BTC. In total, I hold the keys to 2.2 BTC. I want to send 2.1 BTC to Address 4. I will create a transaction as follows:

-   Input 1: 1 BTC from Address 1
-   Input 2: 0.4 BTC from Address 2
-   Input 3: 0.8 BTC from Address 3
-   Output 1: 2.1 BTC to Address 4
-   Output 2. 0.1 BTC to Address 1 (returning the change to the sender)

Once the transaction is digitally signed, published, accepted into a block, and confirmed on the blockchain the ledgers of each address are effectively updated. Address 1 holds 0.1 BTC and addresses 2 and 3 hold 0 BTC. If I were to create a new transaction that tries to send BTC from Address 2, it would be rejected by the nodes because a previous block has confirmed that this address holds 0 BTC.

For further intuition, imagine using physical cash at a corner store. You're buying a bottle of Coke for $1.55. To complete this transaction, you hand the cashier six quarters and a dime (seven inputs). She deposits the cash in the till (output 1) and returns a nickel to you (output 2). This is a more efficient system than trying to pay for everything with pennies, even though with pennies you would never have to make change.

### 10. Privacy

Traditional banking maintains privacy by limiting who can see the transaction history of accounts. This requires the account owner to trust that the bank will abide by this privacy policy. This can't be done for Bitcoin because the protocol requires that all transactions are announced publicly to the entire network. However, the users on the network are effectively pseudonymous, only identifiable by their public keys.

In practice, this pseudonymity can be broken. If a public key is linked to an individual, one could explore the blockchain and see where this public key has previously been used in a transaction. If it was used as an input in a multi-input transaction, it can be inferred that the other keys used in the other inputs are owned by the same person.

Privacy is not guaranteed by the network, but if a user is careful with how they engage with the network (i.e. using a new private/public key pair for each transaction; not linking public keys to their real name) they can effectively remain pseudonymous to the rest of the users.

### 11. Calculations

Satoshi makes some estimates of the probability of success in the event that an attacker tries to defraud the network. Far more in-depth analysis has been performed in the years since the whitepaper was published. I won't present the math here but curious readers can review it in the whitepaper if they wish. The gist is that the attacker would need to control a majority of the computational power on the network to have a hope of achieving their ends. This is now known as a "51% attack" and is considered by some to be an existential threat to the Bitcoin network.

These days, due to the hash rate of the Bitcoin network, for a person or group of people to attempt a 51% attack they would need to spend millions or billions of dollars on computers and electricity for a chance at controlling the network. Even if they did control the network, they couldn't create more bitcoins out of thin air or seize bitcoins that they never controlled. They could unspend bitcoins that they previously spent, but not too far in the past. The further back in the blockchain they want to go, the larger percentage of the computational power they need to control to have a reasonable probability of making back their enormous capital investment. Even then, other nodes on the network could notice an attack happening and the existence of the threat could erase a large amount of Bitcoin's value, further disincentivizing an attacker with a significant capital investment in the network. You must make the network stronger in order to attack it; it's an ingenious security paradigm.

### 12. Conclusion

The Bitcoin whitepaper presents a trust-less system for electronic transactions. Similar decentralized systems of digital coins had been proposed previously, but Bitcoin solves the double-spending problem by using a peer-to-peer network with a public ledger that is secured by the proof-of-work algorithm. In this way, an unstructured, minimally coordinated network is formed where consensus is reached by voting with computational power.

## Further intuition

I hope that the summary of the Bitcoin whitepaper was helpful for gaining a more thorough understanding of how the Bitcoin network works. However, a reader may be left wondering: "what exactly is a bitcoin?"

It's an understandable question because we're used to thinking about money with a physical embodiment. We use coins and bills at a store; even when we interact electronically we usually use a plastic card. Is bitcoin a file on a computer? Can it be corrupted or destroyed?

The answer to both questions is yes and no. To understand that, let's think about a $5 bill. Is a $5 bill actually $5? No. It represents $5 but if I destroy it I haven't actually removed $5 from the monetary system. That $5 exists on the national treasury ledger and they periodically tell the mint to print more bills.

Bitcoin is the distributed ledger of transactions, also called the blockchain. So it is a computer file, albeit one that has identical copies on thousands of computers. You can hold bitcoin in a digital wallet, essentially a database of the private keys that can sign transactions of bitcoins that are assigned to the corresponding public keys on the blockchain. If the private keys are lost, the bitcoin is effectively destroyed because the owner can no longer transact with it but the coins (chains of digital signatures) exist forever on the blockchain.

In the whitepaper, Satoshi uses the word "Bitcoin" exactly once: in the title. It was his name for the electronic cash protocol. It wasn't until later that people started referring to the transactional tokens in the protocol as "bitcoins". It's still most appropriate to think of Bitcoin as the protocol itself. The tokens are just the negative space around which the protocol is constructed.

## Bitcoin today

Nakamoto made a statement with his choice of timestamp headline from January 3, 2009. Inflation caused by increased money supply does not impact all goods and services in the same way. When money flows from central banks, to commercial banks ("Chancellor on brink of second bailout for banks"), to investors, and finally to consumers, the people at the head of the river have [an arbitrage opportunity](https://river.com/learn/terms/c/cantillon-effect/); they can buy goods and services with the new money supply before inflation has been priced in by consumer demand. It's clear that Nakamoto recognized this problem and thought that a decentralized money owned by its users and with a programmatically fixed issuance was part of the solution. At the very least, it's a more fair way to issue money.

I started investigating Bitcoin in May 2020, a couple months into the COVID-19 pandemic. I watched governments print trillions of dollars in response to the crisis. To be fair, this was a necessary measure. However, it is clear that there's no plan to repay that debt through taxation. The only way out is inflation or default (or a mix of both). I was looking for a way to preserve some capital in an asset that couldn't be seized or inflated away. Eventually, I landed on bitcoin.

I made a small investment and sat on it for about a year. As the pandemic dragged on from months into years, I began a more serious investigation into Bitcoin: its origins, how it works, and why it might be important for the world. I came to realize that this asset is important not just for privileged folks like me who want to preserve some wealth, but for anyone in the world who doesn't have access to a stable currency, a banking system, or both. You don't need government ID to use Bitcoin; you don't need anyone's permission, and no one can stop you or censor you. All you need is an internet connection (or [a satellite receiver](https://blockstream.com/satellite/), or, in a pinch, [a shortwave radio](https://www.cryptovibes.com/blog/2019/02/13/bitcoin-transaction-shortwave-radio/)). This is an immense tool of financial freedom for literally billions of people who have previously been excluded from the global economy simply because they weren't born in the right country.

## Closing thoughts

It's interesting to review this paper in hindsight. The introduction presented a vision for Bitcoin as an "electronic cash system". Satoshi thinks that this system could be useful for micropayments due to its low transaction costs. Ironically, the Bitcoin of today has high transaction costs and it is not used to settle small amounts of value (that is, on the main blockchain; small transactions are instead routed and settled on [the Lightning Network](https://en.wikipedia.org/wiki/Lightning_Network) for very low fees).

This is not a criticism of today's version of Bitcoin, it's more an observation of the fascinating social consequences of having a secure transaction settlement network that is governed by open-source software. It's not owned by a single entity. If you don't like how it operates, you can "fork" the open-source library and build your own version. People who like your new version better can bring their computers over and begin running nodes on your new network, securing transactions for the new currency. They vote with their feet in the sense that they're free to move their computers to whichever network they like the best.

If Bitcoin were controlled by Bitcoin Enterprises Inc. with Satoshi Nakamoto as CEO, perhaps it would be a nimble network with short block times, big block size so that transactions could be settled quickly and cheaply. If this were the case, the proof-of-work would be paired down, or perhaps moved to a different proof mechanism such as proof-of-stake. However, I think that this top-down approach only ensures that the community is less invested in the longevity of the network and therefore less interested in developing it. The organic growth of new protocols by the tree-like branching of software forks is the better way to develop consensus over time. Natural selection will determine which protocols live and which die.

Nakamoto recognized this as well. Even though he had no formal control over the network other than his node, he was still the architect and main contributor to the software in the early years. By late 2010, Bitcoin was beginning to get some public attention. It had also attracted talented coders and cryptographers. It had become the world's first feasible cryptocurrency and in doing so had succeeded in its primary mission to be a system for electronic transactions not reliant on a trusted third party. A little more than two years after the genesis block was created, Satoshi ceased communications with the community and stopped contributing to the Bitcoin Core software. His identity and whereabouts remain a mystery and hopefully, they always will.

> "I've moved on to other things and probably won't be around in the future..."
> 
> -   Satoshi Nakamoto, email to Martti Malmi, May 2011
