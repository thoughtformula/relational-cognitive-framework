"""Bounded RCF 0.3 fixture checker (not a reference implementation).

Run: python tools/check_dynamics.py examples/dynamics.json
Only checks rules its code explicitly implements. It does not verify world truth,
external authority, causal inference, sensor quality, or general conformance.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

DYNAMIC = {
    "decision_context": {"agent_id", "environment_id", "state_ids", "belief_ids", "valuation_ids", "constraint_ids", "permission_ids", "recorded_at"},
    "strategy_run": {"operation_id", "context_id", "status", "started_at", "recorded_at"},
    "deliberation": {"agent_id", "context_id", "goal_ids", "candidate_action_ids", "valuation_ids", "constraint_ids", "decision", "recorded_at"},
    "transition_request": {"action_id", "context_id", "expected_state_ids", "permission_ids", "recorded_at"},
    "transition_result": {"issuer_id", "request_id", "status", "prior_state_ids", "result_state_ids", "event_ids", "recorded_at"},
    "feedback": {"action_id", "result_id", "predicted_effect_ids", "observation_ids", "assessment", "recorded_at"},
    "ordering_edge": {"before_id", "after_id", "kind", "recorded_at"},
}
OPTIONAL = {
    "decision_context": {"world_revision"},
    "strategy_run": {"error"},
    "deliberation": {"selected_action_id", "rationale", "unresolved_ids"},
    "transition_request": {"idempotency_key"},
    "transition_result": {"world_revision", "reason"},
    "feedback": {"belief_revision_ids", "notes"},
    "ordering_edge": set(),
}
ENUMS = {
    "strategy_run": ("status", {"completed", "failed", "abstained"}),
    "deliberation": ("decision", {"selected", "abstained", "deferred"}),
    "transition_result": ("status", {"applied", "rejected", "unknown"}),
    "feedback": ("assessment", {"matches", "mismatch", "undetermined"}),
    "ordering_edge": ("kind", {"program_order", "dependency", "serialization", "communication"}),
}
REFERENCE_TYPES = {
    "decision_context": {"agent_id": {"agent"}, "environment_id": {"environment"}, "state_ids": {"state"}, "belief_ids": {"belief"}, "valuation_ids": {"valuation"}, "constraint_ids": {"constraint"}, "permission_ids": {"permission"}},
    "strategy_run": {"operation_id": {"cognitive_operation"}, "context_id": {"decision_context"}},
    "deliberation": {"agent_id": {"agent"}, "context_id": {"decision_context"}, "goal_ids": {"goal"}, "candidate_action_ids": {"action"}, "valuation_ids": {"valuation"}, "constraint_ids": {"constraint"}, "selected_action_id": {"action"}, "unresolved_ids": {"value_conflict"}},
    "transition_request": {"action_id": {"action"}, "context_id": {"decision_context"}, "expected_state_ids": {"state"}, "permission_ids": {"permission"}},
    "transition_result": {"issuer_id": {"entity", "agent"}, "request_id": {"transition_request"}, "prior_state_ids": {"state"}, "result_state_ids": {"state"}, "event_ids": {"event"}},
    "feedback": {"action_id": {"action"}, "result_id": {"transition_result"}, "predicted_effect_ids": {"proposition"}, "observation_ids": {"observation"}, "belief_revision_ids": {"belief_revision"}},
    "ordering_edge": {"before_id": {"action_event", "strategy_run", "transition_request", "transition_result", "feedback"}, "after_id": {"action_event", "strategy_run", "transition_request", "transition_result", "feedback"}},
}


def instant(s):
    if not isinstance(s,str) or not s.endswith('Z'):
        raise ValueError('Instant must be a UTC Z string')
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def cycles(graph):
    visiting, done = set(), set()
    def dfs(node):
        if node in visiting: return True
        if node in done: return False
        visiting.add(node)
        for other in graph.get(node, []):
            if dfs(other): return True
        visiting.remove(node)
        done.add(node)
        return False
    return any(dfs(node) for node in graph)


def validate(bundle):
    errors=[]
    def bad(path,msg): errors.append(f'{path}: {msg}')
    if not isinstance(bundle,dict) or bundle.get('rcf_version') != '0.3.0':
        return ['bundle: expected rcf_version 0.3.0']
    records=bundle.get('records')
    if not isinstance(records,list):return ['bundle: records must be an array']
    index={}
    for i,r in enumerate(records):
        if not isinstance(r,dict):bad(str(i),'not a record');continue
        rid=r.get('id');ty=r.get('type')
        if not isinstance(rid,str) or not rid:bad(str(i),'missing/nonstring id');continue
        if rid in index:bad(rid,'duplicate identifier');continue
        if not isinstance(ty,str) or not ty:bad(rid,'missing type');continue
        index[rid]=r
    def lookup(rid,types=None):
        rec=index.get(rid)
        return rec if rec is not None and (types is None or rec.get('type') in types) else None
    for rid,r in index.items():
        ty=r['type']
        if ty in DYNAMIC:
            missing=DYNAMIC[ty]-set(r)
            if missing:bad(rid,'missing fields '+', '.join(sorted(missing)))
            extra=set(r)-DYNAMIC[ty]-OPTIONAL[ty]-{'id','type'}
            if extra:bad(rid,'unsupported fields '+', '.join(sorted(extra)))
            if ty in ENUMS:
                field,allowed=ENUMS[ty]
                if r.get(field) not in allowed:bad(rid,'invalid '+field)
            for field,types in REFERENCE_TYPES[ty].items():
                if field not in r:continue
                value=r[field]
                refs=value if isinstance(value,list) else [value]
                for ref in refs:
                    if not isinstance(ref,str) or not lookup(ref,types):bad(rid,f'{field} invalid reference {ref!r}')
        if 'recorded_at' in r:
            try:instant(r['recorded_at'])
            except (ValueError,TypeError):bad(rid,'invalid recorded_at')
        if 'valid_during' in r:
            iv=r['valid_during']
            if isinstance(iv,dict):
                try:
                    a=instant(iv['start']) if iv.get('start') else None
                    b=instant(iv['end']) if iv.get('end') else None
                    if a and b and not a < b:bad(rid,'invalid interval')
                except (ValueError,TypeError,KeyError):bad(rid,'invalid interval instant')
            else:bad(rid,'invalid interval object')
    def valid_lists(r,fields):
        for field in fields:
            if not isinstance(r.get(field),list):bad(r['id'],f'{field} must be array')
    for rid,r in index.items():
        ty=r['type']
        if ty not in DYNAMIC:continue
        try:
            if ty=='decision_context':
                valid_lists(r,['state_ids','belief_ids','valuation_ids','constraint_ids','permission_ids'])
                for sid in r.get('state_ids',[]):
                    state=lookup(sid,{'state'})
                    if state and state['environment_id']!=r['environment_id']:bad(rid,'state from other environment')
                for bid in r.get('belief_ids',[]):
                    b=lookup(bid,{'belief'})
                    if b and b['agent_id']!=r['agent_id']:bad(rid,'belief held by other agent')
            elif ty=='strategy_run':
                op=lookup(r.get('operation_id'),{'cognitive_operation'})
                ctx=lookup(r.get('context_id'),{'decision_context'})
                if op and ctx and op['agent_id']!=ctx['agent_id']:bad(rid,'operation/context agent mismatch')
                if instant(r['started_at'])>instant(r['recorded_at']):bad(rid,'run ends before starting')
                if op and r.get('status')=='completed' and any(output not in index for output in op.get('output_ids',[])):bad(rid,'missing completed output')
            elif ty=='deliberation':
                ctx=lookup(r.get('context_id'),{'decision_context'})
                if ctx and ctx['agent_id']!=r.get('agent_id'):bad(rid,'context/agent mismatch')
                valid_lists(r,['goal_ids','candidate_action_ids','valuation_ids','constraint_ids'])
                for aid in r.get('candidate_action_ids',[]):
                    a=lookup(aid,{'action'})
                    if a and a['actor_id']!=r.get('agent_id'):bad(rid,'other-agent candidate')
                if r.get('decision')=='selected':
                    if not r.get('selected_action_id') or r['selected_action_id'] not in r.get('candidate_action_ids',[]):bad(rid,'selected action not in candidate set')
                elif 'selected_action_id' in r:bad(rid,'nonselected deliberation has selected action')
            elif ty=='transition_request':
                act=lookup(r.get('action_id'),{'action'});ctx=lookup(r.get('context_id'),{'decision_context'})
                if act and ctx and (act['actor_id']!=ctx['agent_id'] or act['environment_id']!=ctx['environment_id']):bad(rid,'action/context mismatch')
                valid_lists(r,['expected_state_ids','permission_ids'])
                for sid in r.get('expected_state_ids',[]):
                    s=lookup(sid,{'state'})
                    if s and act and s['environment_id']!=act['environment_id']:bad(rid,'expected state in other environment')
                for pid in r.get('permission_ids',[]):
                    p=lookup(pid,{'permission'})
                    if p and act:
                        fields=[p.get('grantee_id')==act.get('actor_id'),p.get('capability_id')==act.get('capability_id'),p.get('environment_id')==act.get('environment_id'),set(act.get('target_ids',[])).issubset(set(p.get('target_ids',[]))),p.get('effect')=='allow']
                        if not all(fields):bad(rid,'permission not applicable to action')
                        if 'valid_during' in p:
                            now=instant(r['recorded_at']);iv=p['valid_during']
                            if iv.get('start') and now<instant(iv['start']):bad(rid,'grant not yet valid')
                            if iv.get('end') and now>=instant(iv['end']):bad(rid,'grant expired')
            elif ty=='transition_result':
                valid_lists(r,['prior_state_ids','result_state_ids','event_ids'])
                if r.get('status')=='applied' and not (r.get('result_state_ids') or r.get('event_ids')):bad(rid,'applied without attributable change')
                if r.get('status')=='rejected' and (r.get('result_state_ids') or r.get('event_ids')):bad(rid,'rejected with attributed effects')
                if r.get('status')=='unknown' and (r.get('result_state_ids') or r.get('event_ids')):bad(rid,'unknown with asserted effects')
            elif ty=='feedback':
                valid_lists(r,['predicted_effect_ids','observation_ids'])
                res=lookup(r.get('result_id'),{'transition_result'})
                req=lookup(res['request_id'],{'transition_request'}) if res else None
                if req and req['action_id']!=r.get('action_id'):bad(rid,'feedback action/result mismatch')
                if r.get('assessment') in {'matches','mismatch'} and not r.get('observation_ids'):bad(rid,'definite assessment without observation')
        except (KeyError,ValueError,TypeError) as ex:
            bad(rid,'malformed fields: '+str(ex))
    graph=defaultdict(list)
    for r in index.values():
        if r.get('type')=='ordering_edge':
            a,b=r.get('before_id'),r.get('after_id')
            if a==b:bad(r['id'],'ordering self-cycle')
            if a and b:graph[a].append(b)
    if cycles(graph):bad('ordering','cycle in happens-before graph')
    for r in index.values():
        if r.get('type')=='belief_revision':
            prior=lookup(r.get('prior_belief_id'),{'belief'})
            result=lookup(r.get('result_belief_id'),{'belief'})
            if not prior or not result:
                bad(r['id'],'belief revision missing prior or result belief')
                continue
            if prior.get('agent_id')!=result.get('agent_id') or prior.get('proposition_id')!=result.get('proposition_id') or prior.get('agent_id')!=r.get('agent_id'):
                bad(r['id'],'belief revision crosses agent or proposition')
            if result.get('supersedes')!=prior['id']:bad(r['id'],'revision predecessor not preserved')
            if instant(result['recorded_at'])<instant(prior['recorded_at']):bad(r['id'],'belief revision time reversal')
            for trigger in r.get('trigger_ids',[]):
                if trigger not in index:bad(r['id'],'unresolved revision trigger')
    status_paths=defaultdict(list)
    for r in index.values():
        if r.get('type')=='action_event':status_paths[r['action_id']].append(r)
    allowed={'proposed':{'approved','cancelled'},'approved':{'executing','cancelled'},'executing':{'completed','failed','cancelled'},'completed':{'verified'},'verified':set(),'failed':set(),'cancelled':set()}
    for aid,path in status_paths.items():
        path.sort(key=lambda e:(e['recorded_at'],e['id']))
        for i,ev in enumerate(path):
            if i and ev['status'] not in allowed.get(path[i-1]['status'],set()):bad(aid,f'invalid event {path[i-1]["status"]} → {ev["status"]}')
    return errors


def main(path):
    b=json.loads(Path(path).read_text())
    errs=validate(b)
    if errs:
        for e in errs:print('FAIL:',e)
        raise SystemExit(1)
    print(f'PASS: {len(b["records"])} records passed bounded RCF 0.3 structural/dynamics fixture checks')
    print('LIMITATION: external authority, world truth, general conformance and empirical causality were NOT verified')

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'examples/dynamics.json')
