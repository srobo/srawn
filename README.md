# SR(A)WN

**Student Robotics (Almost) Weekly Newsletter**

This is a regular newsletter that is sent out on the mailing list to keep volunteers up to date with what's going on.

## Archive

This repository contains an archive of all internal newsletters that have been sent out. Due to timings and other factors, a few issues are missing their raw pre-email files, however the emails are still available on the list.

The newsletters are grouped by the Student Robotics competition year at which they were sent out.

## Rendering the newsletters

Requires: yarn, python 3,

Install dependencies

```
yarn install
pip install -r requirements.txt
```

Build all: `./scripts/render-all.sh`

Lint filenames: `./scripts/lint-filenames.py`

## How to SR(A)WN

1. Write an entry in `SRYYYY/YYYY-MM-DD-srawn-NN.md`, substituting the programme year, calendar year, day, month, and issue number within the programme year (e.g. `SR2024/2023-11-05-srawn-03.md`).
2. Merge into `main`. This automatically updates the website.
3. Locally, run `scripts/render-all.sh`. This will generate the HTML email in `out/html/SRYYYY/2023-11-05-srawn-03.html`.
4. Open that file locally in Google Chrome. Copy it (formatted).
5. Open SR gmail. Copy and paste the formatted contents into a new email.
6. Set the subject line of the email to "SRAWN SRYYYY Issue NN", substituting the programme year and issue number.
7. Set the To: field to srawn@googlegroups.org
8. Send.
