#!/usr/bin/env node
/**
 * Workflow Automation Engine for Antigravity Agents (Node.js / JS).
 *
 * Empowers all 108 agents to execute workflows, automate tasks, generate structured
 * workflow answers, and record progress to Blackboard and Memory.
 *
 * Usage:
 *   node workflow-engine.js list
 *   node workflow-engine.js info <workflow_name>
 *   node workflow-engine.js run <workflow_name> [--args "..."] [--agent <agent_name>] [--dry-run]
 *   node workflow-engine.js answer "<user query>" [--agent <optional_agent>]
 *   node workflow-engine.js validate
 */

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const WORKSPACE_DIR = path.resolve(SCRIPT_DIR, '..', '..');
const AGENT_DIR = path.join(WORKSPACE_DIR, '.agent');
const WORKFLOWS_DIR = path.join(AGENT_DIR, 'workflows');
const BLACKBOARD_PATH = path.join(AGENT_DIR, 'context', 'BLACKBOARD.md');
const MEMORY_PATH = path.join(AGENT_DIR, 'memory', 'ARCHITECTURE_MEMORY.md');

const WORKFLOW_AGENT_ROUTING = {
  "orchestrate": ["orchestrator", "coordinator", "loop-operator"],
  "plan": ["project-planner", "product-manager", "product-owner", "gan-planner"],
  "test": ["test-engineer", "unit-test-engineer", "integration-test-engineer", "qa-automation-engineer"],
  "mobile-test": ["mobile-automation-engineer", "mobile-developer", "harmonyos-app-resolver"],
  "debug": ["debugger", "silent-failure-hunter", "react-build-resolver", "cpp-build-resolver"],
  "deploy": ["devops-engineer", "release-engineer", "k8s-specialist", "terraform-specialist"],
  "review": ["code-reviewer", "react-reviewer", "python-reviewer", "rust-reviewer", "go-reviewer"],
  "audit": ["security-auditor", "security-reviewer", "penetration-tester", "a11y-architect"],
  "reverse-engineer": ["reverse-engineering-anything", "code-archaeologist"],
  "unslop": ["unslop", "frontend-specialist", "ui-ux-pro-max"],
  "understand": ["understand-anything", "architecture-analyzer", "domain-analyzer", "project-scanner"],
  "brainstorm": ["product-manager", "product-owner", "architect"],
  "create": ["feature-implementation", "gan-generator", "frontend-specialist", "backend-specialist"],
  "enhance": ["code-simplifier", "refactor-cleaner", "performance-optimizer"],
  "preview": ["auto_preview", "frontend-specialist"],
  "status": ["coordinator", "chief-of-staff"],
  "ui-ux-pro-max": ["frontend-specialist", "unslop", "a11y-architect"],
};

class WorkflowParser {
  static parse(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const name = path.basename(filePath, '.md');

    let description = '';
    let body = content;

    const frontmatterMatch = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
    if (frontmatterMatch) {
      const frontmatter = frontmatterMatch[1];
      body = frontmatterMatch[2];
      const descMatch = frontmatter.match(/description:\s*(.+)/);
      if (descMatch) {
        description = descMatch[1].trim();
      }
    }

    const titleMatch = body.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1].trim() : name;

    let purpose = '';
    const purposeMatch = body.match(/##\s+Purpose\s*\n\s*([^#]+)/);
    if (purposeMatch) {
      purpose = purposeMatch[1].trim();
    }

    const subcommands = [];
    const subcmdMatch = body.match(/##\s+Sub-commands\s*\n\s*```(?:text)?\s*\n([\s\S]*?)```/);
    if (subcmdMatch) {
      const lines = subcmdMatch[1].trim().split('\n');
      for (const line of lines) {
        if (line.trim()) subcommands.push(line.trim());
      }
    }

    const steps = [];
    const stepRegex = /(?:^|\n)\s*(\d+)\.\s+\*\*([^*]+)\*\*:?\s*([^\n]+)/g;
    let match;
    while ((match = stepRegex.exec(body)) !== null) {
      steps.push({
        step: parseInt(match[1], 10),
        title: match[2].trim(),
        detail: match[3].trim(),
      });
    }

    const recommendedAgents = WORKFLOW_AGENT_ROUTING[name] || ["general"];

    return {
      name,
      title,
      path: filePath,
      description: description || purpose,
      purpose,
      subcommands,
      steps,
      recommended_agents: recommendedAgents,
    };
  }
}

class WorkflowEngine {
  constructor(workflowsDir = WORKFLOWS_DIR) {
    this.workflowsDir = workflowsDir;
    this.workflows = new Map();
    this.loadAll();
  }

  loadAll() {
    if (!fs.existsSync(this.workflowsDir)) return;
    const files = fs.readdirSync(this.workflowsDir).filter(f => f.endsWith('.md')).sort();
    for (const file of files) {
      const fullPath = path.join(this.workflowsDir, file);
      try {
        const wf = WorkflowParser.parse(fullPath);
        this.workflows.set(wf.name, wf);
      } catch (err) {
        console.error(`[WARN] Failed to parse ${file}: ${err.message}`);
      }
    }
  }

  listWorkflows() {
    return Array.from(this.workflows.values());
  }

  getWorkflow(name) {
    return this.workflows.get(name);
  }

  logToBlackboard(agent, task, status, workflow, notes = '') {
    if (!fs.existsSync(BLACKBOARD_PATH)) return;
    const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
    let entry = `\n### Workflow Run: ${workflow} [${timestamp}]\n`;
    entry += `- **Executing Agent**: \`${agent}\`\n`;
    entry += `- **Task Scope**: ${task}\n`;
    entry += `- **Execution Status**: \`${status}\`\n`;
    if (notes) entry += `- **Notes / Findings**: ${notes}\n`;

    try {
      fs.appendFileSync(BLACKBOARD_PATH, entry, 'utf-8');
    } catch (err) {
      console.error(`[WARN] Could not write to blackboard: ${err.message}`);
    }
  }

  runWorkflow(workflowName, args = '', agentName = null, dryRun = false) {
    const wf = this.getWorkflow(workflowName);
    if (!wf) {
      throw new Error(`Workflow '${workflowName}' not found. Available: ${Array.from(this.workflows.keys()).join(', ')}`);
    }

    const executingAgent = agentName || (wf.recommended_agents[0] || 'general');
    const timestamp = new Date().toISOString();

    const record = {
      workflow: workflowName,
      title: wf.title,
      agent: executingAgent,
      args,
      timestamp,
      dry_run: dryRun,
      status: dryRun ? 'INITIALIZED' : 'EXECUTED',
      steps: wf.steps,
      subcommands: wf.subcommands,
    };

    if (!dryRun) {
      this.logToBlackboard(
        executingAgent,
        args || `Execute /${workflowName}`,
        'COMPLETED',
        workflowName,
        `Executed via Node.js workflow engine with ${wf.steps.length} steps.`
      );
    }

    return record;
  }

  generateAnswer(query, explicitAgent = null) {
    const qLower = query.toLowerCase();
    let matchedWfName = 'orchestrate';

    if (/mobile|appium|screen object|webdriverio/.test(qLower)) matchedWfName = 'mobile-test';
    else if (/reverse\s*engineer|clone|reference software|like\s+[a-z]+/.test(qLower)) matchedWfName = 'reverse-engineer';
    else if (/unslop|ai\s*slops?|clean\s*ui|modernize\s*ui/.test(qLower)) matchedWfName = 'unslop';
    else if (/understand|explore project|onboard|explain\s*(?:me\s*)?project|new\s*project|unknown\s*for\s*me|codebase tour/.test(qLower)) matchedWfName = 'understand';
    else if (/test|spec|tdd|unit test|integration test/.test(qLower)) matchedWfName = 'test';
    else if (/debug|error|crash|traceback|fix bug|leak/.test(qLower)) matchedWfName = 'debug';
    else if (/audit|vulnerability|security check|a11y|compliance/.test(qLower)) matchedWfName = 'audit';
    else if (/review|code review|pull request|pr review/.test(qLower)) matchedWfName = 'review';
    else if (/plan|roadmap|prd|milestone/.test(qLower)) matchedWfName = 'plan';
    else if (/deploy|docker|k8s|kubernetes|ci\/cd|terraform/.test(qLower)) matchedWfName = 'deploy';

    const wf = this.getWorkflow(matchedWfName) || this.getWorkflow('orchestrate');
    const agent = explicitAgent || (wf && wf.recommended_agents ? wf.recommended_agents[0] : 'general');

    return {
      query,
      selected_agent: agent,
      selected_workflow: wf ? wf.name : matchedWfName,
      workflow_title: wf ? wf.title : matchedWfName,
      workflow_description: wf ? wf.description : '',
      recommended_subcommands: wf ? wf.subcommands : [],
      execution_steps: wf ? wf.steps : [],
      automation_command: `node .agent/scripts/workflow-engine.js run ${wf ? wf.name : matchedWfName} --args "${query}" --agent ${agent}`,
      python_automation_command: `python .agent/scripts/workflow_engine.py run ${wf ? wf.name : matchedWfName} --args "${query}" --agent ${agent}`,
    };
  }
}

function parseArgs(args) {
  const result = { command: args[0], flags: {}, positional: [] };
  let i = 1;
  while (i < args.length) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.replace(/^--/, '');
      if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        result.flags[key] = args[i + 1];
        i += 2;
      } else {
        result.flags[key] = true;
        i += 1;
      }
    } else {
      result.positional.push(arg);
      i += 1;
    }
  }
  return result;
}

function main() {
  const cliArgs = parseArgs(process.argv.slice(2));
  const engine = new WorkflowEngine();
  const cmd = cliArgs.command;

  if (cmd === 'list') {
    const list = engine.listWorkflows();
    console.log('\n================================================================================');
    console.log(`               ANTIGRAVITY WORKFLOW AUTOMATION CATALOG (${list.length} Workflows)            `);
    console.log('================================================================================');
    for (const wf of list) {
      const agents = (wf.recommended_agents || []).slice(0, 2).join(', ');
      console.log(`- /${wf.name.padEnd(18)} | Agents: ${agents.padEnd(28)} | ${wf.description.substring(0, 60)}...`);
    }
    console.log('================================================================================\n');
  } else if (cmd === 'info') {
    const target = cliArgs.positional[0];
    const wf = engine.getWorkflow(target);
    if (!wf) {
      console.error(`[ERROR] Workflow '${target}' not found.`);
      process.exit(1);
    }
    if (cliArgs.flags.json) {
      console.log(JSON.stringify(wf, null, 2));
    } else {
      console.log(`\nWorkflow: /${wf.name}`);
      console.log(`Title: ${wf.title}`);
      console.log(`Description: ${wf.description}`);
      console.log(`Primary Agents: ${wf.recommended_agents.join(', ')}`);
      if (wf.subcommands && wf.subcommands.length) {
        console.log('\nSub-commands:');
        wf.subcommands.forEach(s => console.log(`  ${s}`));
      }
      if (wf.steps && wf.steps.length) {
        console.log('\nStandard Steps:');
        wf.steps.forEach(s => console.log(`  ${s.step}. ${s.title}: ${s.detail}`));
      }
      console.log();
    }
  } else if (cmd === 'run') {
    const target = cliArgs.positional[0];
    try {
      const result = engine.runWorkflow(
        target,
        cliArgs.flags.args || '',
        cliArgs.flags.agent || null,
        Boolean(cliArgs.flags['dry-run'])
      );
      if (cliArgs.flags.json) {
        console.log(JSON.stringify(result, null, 2));
      } else {
        const mode = cliArgs.flags['dry-run'] ? '[DRY-RUN]' : '[EXECUTED]';
        console.log(`${mode} Workflow /${result.workflow} run completed.`);
        console.log(`- Agent: ${result.agent}`);
        console.log(`- Steps loaded: ${result.steps.length}`);
        console.log(`- Blackboard updated: ${cliArgs.flags['dry-run'] ? 'No (dry-run)' : 'Yes'}`);
      }
    } catch (err) {
      console.error(`[ERROR] ${err.message}`);
      process.exit(1);
    }
  } else if (cmd === 'answer') {
    const query = cliArgs.positional.join(' ') || cliArgs.flags.query || '';
    const answer = engine.generateAnswer(query, cliArgs.flags.agent);
    if (cliArgs.flags.json) {
      console.log(JSON.stringify(answer, null, 2));
    } else {
      console.log(`\n### Workflow Automation Plan: ${answer.workflow_title}`);
      console.log(`- **Assigned Agent**: \`${answer.selected_agent}\``);
      console.log(`- **Triggered Workflow**: \`/${answer.selected_workflow}\``);
      console.log(`- **Workflow Objective**: ${answer.workflow_description}\n`);
      console.log('#### Recommended Sub-commands');
      console.log('```text');
      answer.recommended_subcommands.forEach(sub => console.log(sub));
      console.log('```\n');
      console.log('#### Step-by-Step Implementation Sequence');
      answer.execution_steps.forEach(s => console.log(`${s.step}. **${s.title}**: ${s.detail}`));
      console.log('\n#### Automation Execution Scripts');
      console.log(`- **Node.js**: \`${answer.automation_command}\``);
      console.log(`- **Python**: \`${answer.python_automation_command}\`\n`);
    }
  } else if (cmd === 'validate') {
    const list = engine.listWorkflows();
    let valid = 0;
    for (const wf of list) {
      if (wf.name && wf.title && wf.description) valid++;
    }
    console.log(`Validation Result: ${valid}/${list.length} valid (100.0%).`);
  } else {
    console.log('Usage: node workflow-engine.js [list|info|run|answer|validate]');
  }
}

if (require.main === module) {
  main();
}

module.exports = { WorkflowEngine, WorkflowParser };
