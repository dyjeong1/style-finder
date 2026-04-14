#!/usr/bin/env bash
set -euo pipefail

REPO_SLUG="${1:-}"
BRANCH_NAME="${2:-main}"
POLICY_PATH="${3:-.github/branch-protection/main.json}"
TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"

if [[ -z "${REPO_SLUG}" ]]; then
  echo "Usage: scripts/apply-branch-protection.sh <owner/repo> [branch] [policy-path]" >&2
  exit 1
fi

if [[ ! -f "${POLICY_PATH}" ]]; then
  echo "Policy file not found: ${POLICY_PATH}" >&2
  exit 1
fi

if [[ -z "${TOKEN}" ]]; then
  echo "Set GITHUB_TOKEN or GH_TOKEN before running this script." >&2
  exit 1
fi

curl --fail --silent --show-error \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/${REPO_SLUG}/branches/${BRANCH_NAME}/protection" \
  --data @"${POLICY_PATH}"

echo
echo "Branch protection applied to ${REPO_SLUG}:${BRANCH_NAME}"
