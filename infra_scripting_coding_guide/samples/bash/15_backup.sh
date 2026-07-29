#!/usr/bin/env bash
# opsctl backup: 指定ディレクトリをアーカイブし、保持期間を超えた古い
# バックアップを削除する。
#
# 警告: --prune は保持期間を超えたバックアップの削除を行う破壊的操作
# である。--dry-run で削除予定を確認してから実行すること。
# --backup-dir は ./backups、./work、/tmp/opsctl-lab 配下に限定する。
set -euo pipefail

backup_dir="backups"
retention_days=14
dry_run=0
prune=0
declare -a source_dirs=()

usage() {
  cat <<'EOF' >&2
Usage: 15_backup.sh --source DIR [--source DIR ...] [--backup-dir DIR] \
       [--retention-days N] [--prune] [--dry-run]
EOF
}

log() {
  local level="$1"; shift
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ${level} $*" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) source_dirs+=("${2:-}"); shift 2 ;;
    --backup-dir) backup_dir="${2:-}"; shift 2 ;;
    --retention-days) retention_days="${2:-}"; shift 2 ;;
    --prune) prune=1; shift ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ "${#source_dirs[@]}" -eq 0 ]]; then
  echo "at least one --source is required" >&2
  usage
  exit 1
fi

case "${backup_dir}" in
  backups|backups/*|./backups|./backups/*|work|work/*|./work|./work/*|/tmp/opsctl-lab|/tmp/opsctl-lab/*)
    ;;
  *)
    echo "--backup-dir must be under ./backups, ./work, or /tmp/opsctl-lab (got: ${backup_dir})" >&2
    exit 1
    ;;
esac

for src in "${source_dirs[@]}"; do
  if [[ ! -d "${src}" ]]; then
    echo "source directory not found: ${src}" >&2
    exit 1
  fi
done

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
archive_name="backup-${timestamp}.tar.gz"
archive_path="${backup_dir}/${archive_name}"

if [[ "${dry_run}" -eq 1 ]]; then
  log INFO "dry-run: would create ${archive_path} from: ${source_dirs[*]}"
else
  mkdir -p "${backup_dir}"
  tar -czf "${archive_path}.tmp" "${source_dirs[@]}"
  mv "${archive_path}.tmp" "${archive_path}"
  log INFO "created ${archive_path}"
fi

if [[ "${prune}" -eq 1 ]]; then
  log INFO "pruning backups older than ${retention_days} days in ${backup_dir}"
  while IFS= read -r -d '' old_file; do
    if [[ "${dry_run}" -eq 1 ]]; then
      log WARNING "dry-run: would delete old backup ${old_file}"
    else
      rm -f -- "${old_file}"
      log WARNING "deleted old backup ${old_file}"
    fi
  done < <(find "${backup_dir}" -maxdepth 1 -name 'backup-*.tar.gz' -mtime "+${retention_days}" -print0 2>/dev/null)
fi

log INFO "backup run finished"
exit 0
