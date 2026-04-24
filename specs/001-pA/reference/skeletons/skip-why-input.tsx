// ──────────────────────────────────────────────────────────
// Skeleton for src/components/skip-why-input.tsx
// Source task: T015 (4-action UI · D16 Layer 3 red-line-2 gate)
// Owner: T015 implementation PR
// How to use: cp this file to src/components/skip-why-input.tsx.
// Style classes are plain strings; T015 will wire Tailwind tokens from
// the design pass — placeholder class names here match action-buttons.tsx.
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/spec.md D16 (skip_why 三层兜底 · this file = Layer 3)
//   - specs/001-pA/reference/api-contracts.md §2.C E10 error codes
//   - specs/001-pA/spec.md §6 O-verify-c6-ui (Playwright verification)
//
// Contract:
//   - Initial render: a single "Skip" button (no textarea visible).
//   - On click → inline expand textarea (focus it) + two buttons: 取消 / 确认.
//   - 确认 button is disabled until `why.trim().length >= 5`.
//   - On success the parent via onSuccess collapses the row.

'use client';

import { useState, useTransition } from 'react';
import {
  recordAction,
  type RecordActionResult,
} from '@/lib/actions/recordAction.js';

type Props = {
  paperId: number;
  /** Called with the result after a successful submit (actionId + optional breadcrumbId). */
  onSuccess: (result: Extract<RecordActionResult, { ok: true }>) => void;
  /** Called with the error result; parent displays toast/banner. */
  onError?: (result: Extract<RecordActionResult, { ok: false }>) => void;
};

const MIN_CHARS = 5;
const MAX_CHARS = 280;

export function SkipWhyInput({ paperId, onSuccess, onError }: Props) {
  const [expanded, setExpanded] = useState(false);
  const [why, setWhy] = useState('');
  const [submitting, startSubmit] = useTransition();

  const trimmed = why.trim();
  const trimmedLen = trimmed.length;
  const valid = trimmedLen >= MIN_CHARS;

  if (!expanded) {
    return (
      <button
        type="button"
        onClick={() => setExpanded(true)}
        className="action-btn action-btn--skip"
        aria-label="Skip this paper"
        data-testid="skip-button"
      >
        Skip
      </button>
    );
  }

  const handleCancel = () => {
    setExpanded(false);
    setWhy('');
  };

  const handleSubmit = () => {
    if (!valid || submitting) return;
    startSubmit(async () => {
      const result = await recordAction({
        paperId,
        action: 'skip',
        why,
      });
      if (result.ok) {
        setExpanded(false);
        setWhy('');
        onSuccess(result);
      } else {
        // TODO(T015): onError may surface toast; for now log to console.
        // biome-ignore lint/suspicious/noConsoleLog: dev fallback until T015 wires log.ts
        console.error('skip failed', result);
        onError?.(result);
      }
    });
  };

  return (
    <div
      className="skip-why-input"
      role="group"
      aria-label="Skip reason"
      data-testid="skip-why-expanded"
    >
      <textarea
        autoFocus
        placeholder="为什么 skip？(至少 5 字符,说清这篇为何信息量不足)"
        value={why}
        onChange={(e) => setWhy(e.target.value)}
        rows={2}
        maxLength={MAX_CHARS}
        data-testid="skip-why-textarea"
      />
      <div className="skip-why-actions">
        <button
          type="button"
          onClick={handleCancel}
          className="action-btn action-btn--ghost"
          disabled={submitting}
        >
          取消
        </button>
        <button
          type="button"
          className="action-btn action-btn--primary"
          disabled={!valid || submitting}
          aria-disabled={!valid || submitting}
          onClick={handleSubmit}
          data-testid="skip-why-submit"
        >
          {submitting ? '提交中…' : `确认 skip (${trimmedLen}/${MIN_CHARS} 字符)`}
        </button>
      </div>
    </div>
  );
}
