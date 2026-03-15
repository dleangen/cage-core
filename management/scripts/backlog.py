#!/usr/bin/env python3
"""
backlog.py — CLI script to manage management/backlog.yaml

Commands:
  list              List all issues (default: all statuses)
  list --status=X   Filter by status (backlog|active|done|cancelled)
  show <id>         Show full detail for an issue
  add               Add a new issue (interactive)
  activate <id>     Set an issue to active (enforces single-active rule)
  done <id>         Mark an issue as done
  cancel <id>       Mark an issue as cancelled
  note <id> <text>  Append a note to an issue

Usage:
  python management/scripts/backlog.py list
  python management/scripts/backlog.py show CORE-0001
  python management/scripts/backlog.py activate CORE-0002
  python management/scripts/backlog.py note CORE-0001 "Some progress note"
"""

import sys
import argparse
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Run: pip install pyyaml")
    sys.exit(1)

BACKLOG_PATH = Path(__file__).parent.parent / "backlog.yaml"


def load_backlog():
    with open(BACKLOG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_backlog(data):
    with open(BACKLOG_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def today():
    return date.today().isoformat()


def find_issue(issues, issue_id):
    for issue in issues:
        if issue["id"].upper() == issue_id.upper():
            return issue
    return None


def cmd_list(args):
    data = load_backlog()
    issues = data.get("issues", []) or []
    status_filter = getattr(args, "status", None)

    filtered = [i for i in issues if not status_filter or i["status"] == status_filter]

    if not filtered:
        print("No issues found.")
        return

    print(f"{'ID':<14} {'STATUS':<12} {'TITLE'}")
    print("-" * 70)
    for issue in filtered:
        print(f"{issue['id']:<14} {issue['status']:<12} {issue['title']}")


def cmd_show(args):
    data = load_backlog()
    issue = find_issue(data.get("issues", []) or [], args.id)
    if not issue:
        print(f"Issue {args.id} not found.")
        sys.exit(1)

    print(f"ID:          {issue['id']}")
    print(f"Title:       {issue['title']}")
    print(f"Status:      {issue['status']}")
    print(f"Created:     {issue['created']}")
    print(f"Updated:     {issue['updated']}")
    print(f"Description: {issue.get('description', '').strip()}")

    notes = issue.get("notes", [])
    if notes:
        print("\nNotes:")
        for note in notes:
            print(f"  [{note['date']}] {note['text']}")


def cmd_activate(args):
    data = load_backlog()
    issues = data.get("issues", []) or []

    active = [i for i in issues if i["status"] == "active"]
    if active:
        print(f"Error: {active[0]['id']} is already active. Complete or cancel it first.")
        sys.exit(1)

    issue = find_issue(issues, args.id)
    if not issue:
        print(f"Issue {args.id} not found.")
        sys.exit(1)

    issue["status"] = "active"
    issue["updated"] = today()
    save_backlog(data)
    print(f"Activated {issue['id']}: {issue['title']}")


def cmd_done(args):
    data = load_backlog()
    issue = find_issue(data.get("issues", []) or [], args.id)
    if not issue:
        print(f"Issue {args.id} not found.")
        sys.exit(1)

    issue["status"] = "done"
    issue["updated"] = today()
    save_backlog(data)
    print(f"Marked done: {issue['id']}: {issue['title']}")


def cmd_cancel(args):
    data = load_backlog()
    issue = find_issue(data.get("issues", []) or [], args.id)
    if not issue:
        print(f"Issue {args.id} not found.")
        sys.exit(1)

    issue["status"] = "cancelled"
    issue["updated"] = today()
    save_backlog(data)
    print(f"Cancelled: {issue['id']}: {issue['title']}")


def cmd_note(args):
    data = load_backlog()
    issue = find_issue(data.get("issues", []) or [], args.id)
    if not issue:
        print(f"Issue {args.id} not found.")
        sys.exit(1)

    if "notes" not in issue or issue["notes"] is None:
        issue["notes"] = []

    issue["notes"].append({"date": today(), "text": args.text})
    issue["updated"] = today()
    save_backlog(data)
    print(f"Note added to {issue['id']}.")


def cmd_add(args):
    data = load_backlog()
    issues = data.get("issues", []) or []

    existing_ids = [i["id"] for i in issues]
    nums = []
    for eid in existing_ids:
        try:
            nums.append(int(eid.split("-")[-1]))
        except ValueError:
            pass
    next_num = (max(nums) + 1) if nums else 1
    prefix = existing_ids[0].rsplit("-", 1)[0] if existing_ids else "CORE"
    new_id = f"{prefix}-{next_num:04d}"

    title = input("Title: ").strip()
    description = input("Description: ").strip()

    new_issue = {
        "id": new_id,
        "title": title,
        "status": "backlog",
        "created": today(),
        "updated": today(),
        "description": description,
        "notes": [],
    }

    issues.append(new_issue)
    data["issues"] = issues
    save_backlog(data)
    print(f"Added {new_id}: {title}")


def main():
    parser = argparse.ArgumentParser(description="CAGE backlog manager")
    subparsers = parser.add_subparsers(dest="command")

    p_list = subparsers.add_parser("list", help="List issues")
    p_list.add_argument("--status", help="Filter by status")
    p_list.set_defaults(func=cmd_list)

    p_show = subparsers.add_parser("show", help="Show issue detail")
    p_show.add_argument("id", help="Issue ID")
    p_show.set_defaults(func=cmd_show)

    p_add = subparsers.add_parser("add", help="Add a new issue")
    p_add.set_defaults(func=cmd_add)

    p_activate = subparsers.add_parser("activate", help="Activate an issue")
    p_activate.add_argument("id", help="Issue ID")
    p_activate.set_defaults(func=cmd_activate)

    p_done = subparsers.add_parser("done", help="Mark issue as done")
    p_done.add_argument("id", help="Issue ID")
    p_done.set_defaults(func=cmd_done)

    p_cancel = subparsers.add_parser("cancel", help="Cancel an issue")
    p_cancel.add_argument("id", help="Issue ID")
    p_cancel.set_defaults(func=cmd_cancel)

    p_note = subparsers.add_parser("note", help="Append a note to an issue")
    p_note.add_argument("id", help="Issue ID")
    p_note.add_argument("text", help="Note text")
    p_note.set_defaults(func=cmd_note)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
