# Rootmoss

**Your AI keeps forgetting you. Your files don't.**

**Your memories, in files you own.**

An **AGENTS.md template** for a personal AI memory — a folder of
plain Markdown your agent reads at session start, so it remembers
you across chats, models and tools. See the
[landing page](https://siagimir.github.io/rootmoss/).

Every chat starts from zero: you re-explain who you are, what you
decided, what matters to you. Rootmoss gives any AI agent a memory
that doesn't reset — a folder of plain Markdown it reads at session
start. Your memories stay on your disk, in files you can copy and
back up — they never get locked inside a chat vendor's memory.
Change the model, the tool, even the company behind it — your
history comes with you.

- **Better conversations from the first message** — your agent starts
  with your profile, your open topics, what you learned last time.
- **Truly yours** — plain files, no Rootmoss account, no
  subscription, no lock-in: your data never lives only inside a
  vendor's product.
- **It compounds** — chats stay disposable; what you save keeps
  paying off as your tree grows.

Works with [OpenCode](https://opencode.ai) — **terminal, desktop app
or web** — or any agent that reads `AGENTS.md`. Open the folder like
any folder: Finder is enough. [Obsidian](https://obsidian.md) or Zed
is optional, if you want a nicer view.

> Status: **experimental / early**. The name and logo are not covered
> by the license.

## What you get

| Piece                | What it does for you                           |
| -------------------- | ---------------------------------------------- |
| `AGENTS.md`          | The contract your agent reads at session start |
| `opencode.json`      | The permission floor — what it may do without  |
|                      | asking you (`edit: ask`, `bash: ask`)          |
| `FIRST-TIME-HERE.md` | Full tour: concepts, FAQ, first steps          |
| `USER.md`            | Your thin profile — the agent's starting point |
| `memory/<6 types>/`  | Typed folders: facts, preferences, decisions,  |
|                      | assumptions, lessons, context                  |
| `inbox/`             | Staging for chats that fit no topic yet        |
| `topics/`            | One folder per life subject, each `topic.md`   |
| `skills/`            | Portable procedures your agent follows         |
| `topics/plants/`     | A fictional demo topic showing the pattern     |

## Prerequisites

- [OpenCode](https://opencode.ai/v2/docs) — desktop app, terminal or
  web; about 5 minutes to install
- `git` — or skip it and use **Download ZIP** (updates get harder
  without git)
- Optional: [Obsidian](https://obsidian.md) or Zed — Finder is enough

First run takes about **15 minutes**.

## Quickstart

**Not technical? Only steps 1–4 are, and they happen once.** Hand
this README to someone who has run `git clone` before — they will be
done in about fifteen minutes. Step 5 is yours, and step 5 is just
pasting a message. Everything after that is conversation.

1. Click **Use this template** → create your own **private** repo.
   Private means only you can see it online — but your host still
   stores the files, so keep raw sensitive documents (bank exports,
   scans, IDs) out of any cloud repo.
2. Get the files — clone it, or **Download ZIP** if you'd rather not
   use `git`:

   ```bash
   git clone <your-repo-url> rootmoss
   cd rootmoss
   ```

3. Install OpenCode — pick whichever suits you:

   - **Desktop app** (no terminal): download from
     [opencode.ai](https://opencode.ai/v2/docs) and install.
   - **Terminal**:

     ```bash
     brew install anomalyco/tap/opencode-v2   # macOS (recommended)
     npm install -g @opencode/cli             # any platform
     curl -fsSL https://opencode.ai/v2/install | bash   # Linux/macOS
     ```

   - **Web**: OpenCode also runs as a web app — needs a one-time
     setup by someone technical; after that, daily use is just a
     browser tab.

4. Start it **from inside the folder**: run `opencode` in the
   terminal, or open the folder in the desktop app.
5. Paste your first message:

   ```text
   Read AGENTS.md and FIRST-TIME-HERE.md. Then interview me one
   question at a time to fill in USER.md, and propose my first topic
   based on what I tell you.
   ```

Then work through `FIRST-TIME-HERE.md` — folders, memory types, and the
rules your agent follows.

## Who this is not for

- You want a polished app with accounts and sync — this is a folder.
- You never want to set anything up — daily use can be terminal-free
  (desktop app or web), but the one-time setup still takes about 15
  minutes; have someone technical do it once.

## Storage is your choice

Rootmoss is a folder — it doesn't host, sync, encrypt or back up
anything. Where your copy lives (local disk, GitHub, a NAS,
self-hosted git), what you back it up to and what you encrypt is up
to you. The docs recommend patterns; no host or tool can guarantee
them. If your notes matter, keep more than one copy: the classic
rule is **3-2-1** — three copies, two kinds of media, one offsite.
A good plain-language explanation: [Backblaze on the 3-2-1
rule][321].

The backup part is on you — same for the AI provider you connect:
your account, your terms. One thing always travels: when your agent
reads a note, that text goes to the model you connected, exactly as
it would in any AI chat. Your folder stays put; the words it reads
travel.

[321]: https://www.backblaze.com/blog/the-3-2-1-backup-strategy/

## Support

Experimental. "Where did I get stuck?" issues are the most welcome
contribution; responses are best-effort, not guaranteed.

## Updates

Releases are announced on the repo's **Releases** page. To get an
email per release: **Watch** the repo → *Custom* → *Releases* →
*Notify me when releases are published*. Or check `CHANGELOG.md`
before pulling (`FIRST-TIME-HERE.md` §8).

## License

[MIT](LICENSE) — code and prose. The Rootmoss **name and logo** are not
covered by the license; please don't publish confusingly similar
derivatives under this name.
