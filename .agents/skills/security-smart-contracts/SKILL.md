---
name: security-smart-contracts
description: Companion overlay for the local `security` workflow skill when reviewing or implementing Solidity or EVM smart contracts. Use with `security` for on-chain value flows, privileged roles, external calls, oracle assumptions, upgradeability, and exploit patterns such as reentrancy and front-running.
---

# Security Smart Contracts

Use this companion overlay with `security` when the task involves Solidity or
EVM smart contracts.

## Focus areas

- privileged roles, admin keys, upgrade paths, and pause or rescue powers
- asset and value flows across deposits, withdrawals, minting, liquidation, or
  settlement paths
- external calls, callbacks, token hooks, and cross-contract assumptions
- oracle, bridge, relayer, and off-chain signer trust boundaries
- mempool visibility, front-running, sandwiching, replay, and signature misuse

## Not For

- generic Solidity style review with no security objective
- gas-only optimization work where value-flow or privilege assumptions are unchanged
- blockchain product discussion detached from concrete contracts or trust boundaries

## Workflow

1. Map privileged actors and value flows:
   who can move funds, mint, burn, liquidate, pause, upgrade, or change
   configuration.
2. Map trust boundaries:
   external contracts, tokens, hooks, oracles, bridges, relayers, and off-chain
   signers the system depends on.
3. Identify state-transition invariants:
   balances, share accounting, debt or collateral ratios, sequencing
   assumptions, and post-call expectations.
4. Review exploit classes against those flows:
   reentrancy, access-control failures, arithmetic/version issues,
   front-running, replay, oracle manipulation, and unsafe external-call
   handling.
5. Report by asset at risk:
   fund loss, privilege escalation, griefing, governance capture, or liveness
   failure, with required attacker capability.

## Review rules

- check reentrancy and enforce checks-effects-interactions or an equivalent
  non-reentrant design
- verify access control on every privileged or state-changing path, including
  upgrade and initialization flows
- prefer pull-over-push payout patterns when funds leave the contract
- inspect arithmetic and compiler-version assumptions, especially for pre-0.8
  code or unchecked blocks
- verify failure handling on external calls and token transfers; do not assume
  ERC-20 compliance is uniform
- examine invariant-sensitive flows for price manipulation, oracle staleness,
  rounding, and share-accounting edge cases

## Threat-model additions

When threat modeling contracts, explicitly map:

1. who can move value, mint, burn, upgrade, pause, or change critical config
2. where user-controlled calldata or signatures influence value movement
3. which external contracts, tokens, or oracles are trusted
4. what happens if a dependency reverts, lies, lags, or reenters
5. which assumptions depend on mempool ordering or off-chain actors

## Reporting rules

- report asset at risk, exploitable path, and required attacker capabilities
- distinguish direct fund-loss paths from governance, griefing, or liveness
  risks
- call out assumptions about token behavior, decimals, callbacks, and oracle
  freshness explicitly
