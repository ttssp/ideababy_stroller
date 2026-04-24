// ──────────────────────────────────────────────────────────
// Skeleton for src/app/(main)/today/today-client.tsx
// Source task: T014 (/today interactive layer) + T015 (action buttons)
// Owner: T014 implementation PR
// How to use: cp this file to src/app/(main)/today/today-client.tsx.
// Server-side data is passed in via props (never re-fetches in the client).
// Do NOT edit the file in specs/; edit the copy in src/.
// ──────────────────────────────────────────────────────────
//
// Authoritative references:
//   - specs/001-pA/reference/api-contracts.md §3.6 (BriefingItem shape)
//   - specs/001-pA/spec.md IN-3 (4-action UI)
//   - specs/001-pA/reference/directory-layout.md §1 (sibling components)

'use client';

import { useState } from 'react';
import { SkipWhyInput } from '@/components/skip-why-input.js';
import type { BriefingItem } from '@/lib/briefings/types.js';
import type { RecordActionResult } from '@/lib/actions/recordAction.js';
import { recordAction } from '@/lib/actions/recordAction.js';

type Props = {
  seat: { id: number; email: string; role: 'admin' | 'member' };
  forDate: string; // 'YYYY-MM-DD'
  items: BriefingItem[];
  staleDate: boolean;
};

export function TodayClient({ seat, forDate, items, staleDate }: Props) {
  // Optimistic local overrides so the row visibly updates without a refetch.
  const [localActions, setLocalActions] = useState<Record<number, string>>({});

  const onActionDone = (paperId: number) => (result: RecordActionResult) => {
    if (result.ok) {
      // TODO(T015): look up the server-returned action; for now assume input action.
      // This happy-path only marks the row as "acted on".
      setLocalActions((prev) => ({ ...prev, [paperId]: 'done' }));
    }
  };

  return (
    <main className="today-page" data-testid="today-root">
      <header className="today-header">
        <h1>今日 briefing · {forDate}</h1>
        <div className="today-meta">
          <span>seat: {seat.email}</span>
          <span>role: {seat.role}</span>
        </div>
        {staleDate && (
          <div className="stale-banner" role="alert">
            worker 昨夜未成功,当前 briefing 来自 {forDate} —— 请联系 operator。
          </div>
        )}
      </header>

      <section className="today-items">
        {items.length === 0 ? (
          <p>今天暂无 state shift —— 所有 topic 稳定。</p>
        ) : (
          items.map((item) => (
            <TopicCard
              key={item.topic.id}
              item={item}
              onActionDone={onActionDone}
              locallyActed={localActions}
            />
          ))
        )}
      </section>
    </main>
  );
}

// --------------------------------------------------------------------
// TopicCard · one per topic with ≤ 3 trigger papers
// --------------------------------------------------------------------

function TopicCard({
  item,
  onActionDone,
  locallyActed,
}: {
  item: BriefingItem;
  onActionDone: (paperId: number) => (r: RecordActionResult) => void;
  locallyActed: Record<number, string>;
}) {
  return (
    <article className="topic-card">
      <h2>{item.topic.name}</h2>
      <p className="state-summary">{item.topicStateSummary}</p>
      {item.anchorPaper && (
        <p className="anchor">
          anchor: <a href={`/papers/${item.anchorPaper.id}/history`}>{item.anchorPaper.title}</a>
        </p>
      )}
      <ul className="trigger-papers">
        {item.papers.map((row) => (
          <li key={row.paper.id} className="trigger-paper">
            <a href={`/papers/${row.paper.id}/history`}>{row.paper.title}</a>
            {row.isShift && <span className="badge shift">SHIFT</span>}
            {row.summary && <p className="summary">{row.summary.summaryText}</p>}
            {locallyActed[row.paper.id] ? (
              <span className="acted">已标注</span>
            ) : (
              <ActionRow paperId={row.paper.id} onDone={onActionDone(row.paper.id)} />
            )}
          </li>
        ))}
      </ul>
    </article>
  );
}

// --------------------------------------------------------------------
// ActionRow · 4-action group; Skip routes through SkipWhyInput (D16 Layer 3)
// --------------------------------------------------------------------

function ActionRow({
  paperId,
  onDone,
}: {
  paperId: number;
  onDone: (r: RecordActionResult) => void;
}) {
  const fire = async (action: 'read_now' | 'read_later' | 'breadcrumb') => {
    const result = await recordAction({ paperId, action });
    onDone(result);
  };

  return (
    <div className="action-row" role="group" aria-label="paper actions">
      <button type="button" className="action-btn" onClick={() => fire('read_now')}>
        Read now
      </button>
      <button type="button" className="action-btn" onClick={() => fire('read_later')}>
        Read later
      </button>
      <SkipWhyInput
        paperId={paperId}
        onSuccess={(r) => onDone(r)}
        onError={(r) => onDone(r)}
      />
      <button type="button" className="action-btn" onClick={() => fire('breadcrumb')}>
        Breadcrumb
      </button>
    </div>
  );
}
