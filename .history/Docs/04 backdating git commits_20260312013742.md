# 📅 **Backdating Git Commits - Super Simple Guide**

---

## **What is this?**
Make commits appear on **any past date** on GitHub.

---

## **The Magic Command**
```bash
git commit --date 'YYYY-MM-DD HH:MM:SS' -m "your message"
```

---

## **Quick Examples**

| You Want | Command |
|----------|---------|
| **Today's date** | `git commit -m "message"` |
| **Jan 1, 2026** | `git commit --date '2026-01-01 12:00:00' -m "message"` |
| **Yesterday** | `git commit --date 'yesterday' -m "message"` |
| **5 days ago** | `git commit --date '5 days ago' -m "message"` |
| **Last year** | `git commit --date '2025-03-12' -m "message"` |

---

## **3-Step Workflow**

```bash
# 1. Add your file(s)
git add your-file.txt
or,
git add .

# 2. Commit with past date
git commit --date '2026-01-01 09:30:00' -m "update readme"

# 3. Push to GitHub
git push origin main
```

---

## **Date Formats That Work**
```
'2026-01-01'              (midnight)
'2026-01-01 14:30:00'     (2:30 PM)
'5 days ago'              (relative)
'last week'               (simple English)
'2026-01-01 09:00:00 +0600' (with timezone)
```

---

## **⚠️ Important Rules**
- ✅ Repo must **exist** on that date
- ✅ Works on **any branch**
- ✅ Shows on GitHub contribution graph
- ❌ Can't go before **first commit date**
- ❌ Can't change file's actual modified time

---

## **Check Your Work**
```bash
# Verify commit date
git log --pretty=fuller -n 1
```

---

## **One-Liner Template**
```bash
git add . && git commit --date '2026-01-01' -m "update" && git push
```

---

**That's it!** 🚀 Copy, paste, change the date, and go!