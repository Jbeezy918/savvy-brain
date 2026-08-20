# Sovereign Agents — watchdog, model rotation, voices, dispatch

Builds on the Sovereign Node Suite. Two installers because the two boxes do
different jobs:

| Installer | Runs on | Purpose |
|---|---|---|
| `install_sovereign_agents_mac.sh` | Mac Pro / Mac Air | Watchdog tools, TTS voices, dispatch — Titus/Cassius **off** by default here |
| `install_sovereign_agents_nucbox.sh` | NucBox (Linux Mint) | Titus + Cassius run 24/7 as systemd services — this is the "always on even if my Mac is off" piece |

## Why they're not both always-on everywhere
Running the same agent in two places at once means two processes writing to
`shared_brain.json` at the same time — that's a real risk of corrupted or
conflicting state, not a hypothetical one. Default posture: **one live copy**,
resident on the NucBox since it's the box that's actually always powered.
Mac Pro/Air are on-demand extra compute — `agent-start` or `agent-dispatch`
spins one up there when you want it, `agent-stop` when you're done.

## Commands (Mac side)
| Command | Does |
|---|---|
| `agent-start <name> [job]` | Runs the agent locally under the watchdog |
| `agent-stop <name>` | Stops it |
| `agent-status` | Heartbeat freshness for every registered agent |
| `agent-speak <name> "text"` | Say something in that agent's voice |
| `agent-dispatch <name> <job-type>` | Runs it on whichever cluster node fits the job, using live status from `node-check` |
| `ai-launch <tool>` | Now works for *any* installed CLI (aider, interpreter, titus, cassius, claude, gemini...) — packs code, shows cluster status, launches it |

## Model rotation (job-type → Ollama model)
| Job type | Model | Typical node |
|---|---|---|
| `quick` | neural-chat:7b | NucBox |
| `coding` | qwen2.5-coder:14b | anywhere |
| `deep-coding` | qwen2.5-coder:32b | Mac Pro (36GB RAM) |
| `vision` | llava:34b | Mac Pro |
| `thinking` | deepseek-r1:70b | Mac Pro |

Edit the `case` block in `agent_supervisor.sh` if your actual Ollama tags differ.

## Voices
Titus = male (`Daniel`), Cassius = female (`Samantha`), rate cranked to match
your fast-listening preference. This is macOS `say` — free, built-in, zero
setup, but it still sounds like a computer. Two upgrade paths if you want it
to sound more human:
- **Piper TTS** — free, open-source, runs fully local, noticeably more natural
  than `say`. Best fit for your cost-optimization rule (no subscription).
- **ElevenLabs** — sounds closest to a real human, but it's a paid API and a
  network call per line. Only worth it if voice quality becomes a real
  product/customer-facing need, not for internal alerts.
Say the word and I'll wire either into `agent-speak` in place of `say`.

## Assumptions / things to verify (I can't see your machines from here)
1. `titus` and `cassius` read `$OLLAMA_MODEL` to pick their model. If they
   don't yet, that's a one-line change in their source to respect it — tell
   me and I'll draft the patch once I can see that code.
2. Both commands exist on PATH on whichever node you dispatch to.
3. Passwordless SSH is set up to each node (`sovereign-ssh-setup`, from the
   node suite) — required for `agent-dispatch` to reach a remote box.
4. `python3` is available on the Mac (used to parse cached node status) —
   already true everywhere else in your setup.
5. Long-term memory/learning already lives in `shared_brain.json` + ChromaDB —
   this layer doesn't touch that, it only adds supervision, voice, and
   placement on top. If you want the watchdog itself to log into that same
   store, I'd need to see its schema first so I don't corrupt it.
