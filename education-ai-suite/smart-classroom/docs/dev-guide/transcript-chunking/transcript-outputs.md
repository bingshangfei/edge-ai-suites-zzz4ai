<!-- SPDX-FileCopyrightText: (C) 2026 Intel Corporation -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# The 5 Speech-Transcription Output Files

After a lesson (or an audio session) is transcribed, **5 transcription files** are written under `storage/<session>/raw/`, each for a different purpose. The table below gives a quick overview; each file is explained with its content and format below.

| File | What it is |
|------|-----------|
| `asr_events.jsonl` | Per-chunk transcription records (structured) |
| `transcription.txt` | Full transcript, with speaker labels |
| `transcription_ts.txt` | Full transcript, with timestamps and speaker labels |
| `content_segmentation_transcription.txt` | Transcript for content / topic segmentation |
| `teacher_transcription.txt` | Only what the teacher said |

---

## 1. `asr_events.jsonl` — Record stream of transcription events

One JSON record per audio chunk, containing the chunk's time slice, the transcript text for the slice, and sentence-level detail (speaker, start/end). Useful when a program needs to read the transcript sentence-by-sentence or by timestamp.

Example (one record per line; text is abbreviated):

```json
{"chunk_path": "chunks/chunk_0.wav", "start_time": 0.0, "end_time": 30.0,
 "chunk_index": 0, "text": "SPEAKER_00: ...\n",
 "segments": [{"speaker": "SPEAKER_00", "text": "...", "start": 14.24, "end": 16.3}]}
```

---

## 2. `transcription.txt` — Full transcript (with speakers)

The whole lesson's speech, one line per utterance, prefixed with who spoke (Teacher / Student).

```text
Teacher: Let's read this poem together today.
Student_01: He freesiffed and sang as he walked.
Teacher: Good, a little louder.
```

---

## 3. `transcription_ts.txt` — Full transcript (with timestamps)

Same content as `transcription.txt`, but each line is prefixed with the **start–end time** (in seconds), so you can locate when a sentence was spoken.

```text
[14-16] Teacher: Let's read this poem together today.
[16-19] Student_01: He freesiffed and sang as he walked.
[19-20] Teacher: Good, a little louder.
```

---

## 4. `content_segmentation_transcription.txt` — For segmentation

Usually the same line count as the full transcript, but with **only `[start-end] text` — no speaker label**. Dropping the speaker prefix keeps topic/content segmentation clean, without being swayed by *who* said something.

```text
[14-16] Let's read this poem together today.
[16-19] He freesiffed and sang as he walked.
[19-20] Good, a little louder.
```

---

## 5. `teacher_transcription.txt` — Teacher-only transcript

Contains **only the teacher's** speech, also in `[start-end] text` format. Use it when you want only what the teacher said in the lesson.

```text
[14-16] Let's read this poem together today.
[19-20] Good, a little louder.
[27-28] Class, that's all for today.
```