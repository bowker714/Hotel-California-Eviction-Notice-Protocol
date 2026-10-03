**Title:** Hotel California Eviction Notice Protocol (HCENP): Automated Deep-Metadata Audio Remediation Architecture

**Document ID:** HCENP-2026-v1.0

**Status:** Operational / Production-Ready

---

## Executive Summary

As local music repositories scale, unwanted legacy audio tracks can persist within file trees due to inconsistent naming conventions, obfuscated directory structures, and embedded ID3 tags. The **Hotel California Eviction Notice Protocol (HCENP)** is a Python-based utility designed to identify, flag, and mitigate audio files attributed to the rock band *The Eagles*.

By integrating multi-layered file system traversal with deep metadata extraction via the `mutagen` framework, HCENP ensures complete remediation of undesired media assets while maintaining interactive human-in-the-loop oversight. Additionally, the protocol incorporates a multimodal audio-visual notification trigger referencing *The Big Lebowski* (1998) to provide immediate operator feedback upon execution.

---

## System Architecture & Technical Specifications

```
                          ┌──────────────────────────┐
                          │   Initialization Phase   │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │  Trigger Multimedia AV   │
                          │   (Chrome / Web Browser) │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │ Directory Tree Traversal │
                          │ (~/Music, ~/Downloads)   │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │ Extension Filtering Pass │
                          │ (.mp3, .flac, .m4a, ...) │
                          └─────────────┬────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │  Multi-Tier Evaluation   │
                          └──────┬────────────┬──────┘
                                 │            │
            ┌────────────────────┘            └────────────────────┐
            ▼                                                      ▼
  [Tier 1: Path Inspection]                             [Tier 2: ID3 / Tag Analysis]
  Matches "the eagles" / "eagles"                       Scans artist, album artist,
  in filename or path string                            composer, and raw tag blobs
            │                                                      │
            └────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Match Flagged / Target   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Interactive Confirmation │
                    │ (Yes / No / All / Quit)  │
                    └────────────┬─────────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
          [Delete File Asset]        [Preserve / Skip File]

```

---

## Core Technical Components

### 1. Multimodal Operator Alert Mechanism

Upon invocation, `play_dude_clip()` initiates a browser payload attempting to launch Google Chrome explicitly (across macOS, Windows, and Linux environments) or falling back to the system's default browser. The payload targets a timestamped external reference to set the operational context prior to disk mutation:

$$\text{Target URL} = \texttt{[https://youtu.be/-JlmvtAHhnc?t=21](https://youtu.be/-JlmvtAHhnc?t=21)}$$

### 2. Multi-Tier Target Identification Logic

The detection engine operates via a two-stage evaluation pipeline to ensure high recall across both formatted and unformatted audio files:

* **Tier 1: Filename & Path Evaluation:** Normalizes the absolute path string to lowercase and checks for substring presence against target keywords:
$$\mathcal{K} = \{\text{"the eagles"}, \text{"eagles"}\}$$


* **Tier 2: Deep Tag & Metadata Inspection:** Utilizes the `mutagen` library to extract internal metadata frames (e.g., ID3v2, Vorbis Comments, MP4 Atoms). All metadata values are flattened into a single unified search space $\mathcal{S}_{\text{meta}}$:
$$\mathcal{S}_{\text{meta}} = \bigcup_{k \in \text{Tags}} \text{lowercase}(V_k)$$


If $\exists k \in \mathcal{K}$ such that $k \subseteq \mathcal{S}_{\text{meta}}$, the asset is flagged with the reason `"Metadata/ID3 Tag match"`.

### 3. File Extension Filtering

To optimize disk I/O performance, non-audio files are discarded prior to parsing. The supported media matrix includes:

$$\text{Supported Extensions} = \{\text{.mp3}, \text{.flac}, \text{.m4a}, \text{.wav}, \text{.aac}, \text{.ogg}, \text{.wma}\}$$

### 4. Interactive Human-in-the-Loop Safeguards

To prevent unintended data destruction, identified assets trigger an interactive command-line interface (`confirm_deletion`). The operator can choose from four distinct operational modes:

| Command Key | Action | Scope |
| --- | --- | --- |
| `y` / `yes` | Remediate target file | Current asset only |
| `n` / `no` | Preserve target file | Current asset only |
| `all` | Enable batch remediation | All remaining flagged assets in scan session |
| `q` / `quit` | Immediately terminate process | Halts scan immediately |

---

## Operational Security & Reliability Considerations

1. **Graceful Exception Handling:**
* **Dependency Check:** If `mutagen` is missing at startup, the program terminates with exit code `1` and provides installation guidance (`pip install mutagen`).
* **I/O Resilience:** Errors encountered during metadata parsing or file unlinking (`os.remove`) are caught and logged without crashing the background process.


2. **Missing Path Skipping:** Non-existent directories specified in `SEARCH_DIRECTORIES` are automatically skipped, allowing cross-platform deployment without unhandled path errors.

---

## Deployment & Execution

### Prerequisites

* Python 3.7 or higher
* Mutagen metadata library

```bash
pip install mutagen
python hotel_california_protocol.py

```

---

## Conclusion

The **Hotel California Eviction Notice Protocol** provides a reliable mechanism for targeting and eliminating audio assets associated with *The Eagles*. By combining path analysis with ID3 metadata evaluation, HCENP ensures that target tracks cannot evade removal through file renaming alone, providing a definitive resolution for audio directory maintenance.
