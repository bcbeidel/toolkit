---
name: "Model Context Protocol (MCP) Deep Dive"
description: "Comprehensive investigation of MCP's specification, adoption, server/client patterns, comparison to alternatives, and roadmap"
type: research
sources:
  - https://modelcontextprotocol.io/specification/2025-11-25
  - https://modelcontextprotocol.io/docs/learn/architecture
  - https://modelcontextprotocol.io/specification/2025-11-25/changelog
  - https://modelcontextprotocol.io/development/roadmap
  - https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/
  - https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
  - https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
  - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
  - https://github.com/modelcontextprotocol/modelcontextprotocol
  - https://www.descope.com/blog/post/mcp-vs-function-calling
  - https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
  - https://zilliz.com/blog/function-calling-vs-mcp-vs-a2a-developers-guide-to-ai-agent-protocols
  - https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/
  - https://prompt.security/blog/top-10-mcp-security-risks
  - https://workos.com/blog/mcp-2025-11-25-spec-update
  - https://particula.tech/blog/mcp-developer-guide
  - https://forgecode.dev/blog/mcp-spec-updates/
  - https://en.wikipedia.org/wiki/Model_Context_Protocol
related:
  - docs/research/2026-04-07-cli-tool-design.research.md
  - docs/research/2026-04-07-skill-ecosystem-design.research.md
---

## Research Question

What is MCP's current state — specification, adoption, server/client patterns, competitive position vs. alternative protocols, and where the spec is heading?

## Sub-Questions

1. What is MCP's current specification, adoption trajectory, and governance (AAIF donation, monthly download stats)?
2. How do MCP servers expose tools, resources, and prompts, and what are the protocol's design principles?
3. What patterns exist for building MCP servers vs. consuming them as a client?
4. How does MCP relate to other tool protocols (OpenAI function calling, LangChain tools, Semantic Kernel plugins, A2A)?
5. What are MCP's current limitations and where is the spec heading?

## Search Protocol

| # | Query | Key Finding |
|---|-------|-------------|
| 1 | Model Context Protocol MCP specification 2025-11-25 official spec | Official spec at modelcontextprotocol.io; 2025-11-25 is latest release with Tasks, OAuth overhaul |
| 2 | MCP AAIF Linux Foundation donation governance 2025 | Donated Dec 9 2025; AAIF co-founded by Anthropic, Block, OpenAI; governance unchanged |
| 3 | MCP npm downloads monthly statistics 2025 2026 | 97M monthly SDK downloads by March 2026; 2M at launch Nov 2024 |
| 4 | MCP server primitives tools resources prompts design principles JSON-RPC | Three core primitives (tools/resources/prompts); JSON-RPC 2.0; two transports |
| 5 | MCP Python SDK TypeScript SDK server building patterns examples 2025 | FastMCP (Python) and McpServer+Zod (TypeScript) are standard patterns |
| 6 | MCP client implementation patterns host application Claude Cursor VS Code | Claude, Cursor, VS Code are major hosts; stdio for local, Streamable HTTP for remote |
| 7 | MCP vs OpenAI function calling comparison differences 2025 | MCP: provider-agnostic, modular, server-isolated; function calling: simpler, vendor-specific |
| 8 | MCP vs LangChain tools Semantic Kernel plugins A2A Agent-to-Agent | SK and LangChain are frameworks that can consume MCP; A2A is agent-to-agent (different layer) |
| 9 | MCP limitations problems security vulnerabilities prompt injection 2025 | Tool poisoning, prompt injection, rug pulls, CVE-2025-6514 (mcp-remote RCE) |
| 10 | MCP roadmap 2026 upcoming features specification evolution SEP proposals | 4 priorities: transport scalability, agent comms, governance maturation, enterprise readiness |
| 11 | MCP registry server discovery authorization OAuth 2.1 2025 2026 | OAuth 2.1 + PKCE mandatory for HTTP; /.well-known/oauth-protected-resource discovery |
| 12 | MCP GitHub stars contributors server ecosystem growth statistics 2025 2026 | 7.8k stars on spec repo; servers repo 79k stars; 10,000+ public servers |
| 13 | MCP stateless mode Streamable HTTP production deployment scalability | Stateless Streamable HTTP allows horizontal scaling; serverless-compatible |
| 14 | MCP 2025-06-18 specification release new features elicitation streamable HTTP | June 2025 spec: structured outputs, elicitation, OAuth resource server requirement, removed JSON-RPC batching |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://modelcontextprotocol.io/specification/2025-11-25 | MCP Specification 2025-11-25 | MCP Project | 2025-11-25 | T1 | verified |
| 2 | https://modelcontextprotocol.io/docs/learn/architecture | Architecture Overview | MCP Project | 2025–2026 | T1 | verified |
| 3 | https://modelcontextprotocol.io/specification/2025-11-25/changelog | Key Changes (2025-11-25) | MCP Project | 2025-11-25 | T1 | verified |
| 4 | https://modelcontextprotocol.io/development/roadmap | Roadmap (updated 2026-03-05) | MCP Project | 2026-03-05 | T1 | verified |
| 5 | https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/ | One Year of MCP: November 2025 Spec Release | MCP Project | 2025-11-25 | T1 | verified |
| 6 | https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/ | The 2026 MCP Roadmap | MCP Project | 2026 | T1 | verified |
| 7 | https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation | Donating MCP and Establishing AAIF | Anthropic | 2025-12-09 | T1 | verified |
| 8 | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | Linux Foundation Announces AAIF | Linux Foundation | 2025-12-09 | T1 | verified |
| 9 | https://github.com/modelcontextprotocol/modelcontextprotocol | MCP Specification GitHub Repository | MCP Project | ongoing | T1 | verified |
| 10 | https://www.descope.com/blog/post/mcp-vs-function-calling | MCP vs. Function Calling | Descope | 2025 | T3 | verified |
| 11 | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | Announcing the Agent2Agent Protocol | Google | 2025-04-09 | T1 | verified |
| 12 | https://zilliz.com/blog/function-calling-vs-mcp-vs-a2a-developers-guide-to-ai-agent-protocols | Function Calling vs MCP vs A2A | Zilliz | 2025 | T3 | verified |
| 13 | https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/ | MCP has prompt injection security problems | Simon Willison | 2025-04-09 | T3 | verified |
| 14 | https://prompt.security/blog/top-10-mcp-security-risks | Top 10 MCP Security Risks | Prompt Security | 2025 | T3 | verified |
| 15 | https://workos.com/blog/mcp-2025-11-25-spec-update | MCP 2025-11-25 Spec Update | WorkOS | 2025-11-25 | T3 | verified |
| 16 | https://particula.tech/blog/mcp-developer-guide | MCP Developer Guide: Build Servers, Connect Tools | Particula Tech | 2026 | T3 | verified |
| 17 | https://forgecode.dev/blog/mcp-spec-updates/ | MCP 2025-06-18 Spec Update | ForgeCode | 2025 | T3 | verified |
| 18 | https://en.wikipedia.org/wiki/Model_Context_Protocol | Model Context Protocol | Wikipedia | 2025–2026 | T4 | verified |

## Raw Extracts

### Sub-question 1: Specification, adoption, governance

**Protocol history and versioning**

MCP was announced by Anthropic on November 25, 2024, as an open standard to address "information silos and legacy systems." The protocol reuses message-flow concepts from the Language Server Protocol and is transported via JSON-RPC 2.0.

Three specification versions exist:
- `2024-11-05` — initial release (November 2024)
- `2025-03-26` — introduced Streamable HTTP transport, deprecating SSE as standalone transport
- `2025-06-18` — added structured tool outputs, elicitation, OAuth resource server requirements, removed JSON-RPC batching; added security best practices page
- `2025-11-25` — current release: async Tasks primitive (SEP-1686), simplified OAuth via Client ID Metadata Documents, sampling with tools, URL-mode elicitation, tool naming guidance, OIDC discovery

The schema is defined in TypeScript first, made available as JSON Schema for wider compatibility. The authoritative schema lives at `schema/2025-11-25/schema.ts` in the spec repository.

**Adoption trajectory**

Download growth (SDK, combined Python+TypeScript):
- Nov 2024 launch: ~2M monthly downloads
- Apr 2025 (OpenAI adoption): 22M/month
- Jul 2025 (Microsoft joins): 45M/month
- Nov 2025 (AWS joins): 68M/month
- Mar 2026: 97M/month

For comparison, React took ~3 years to hit 100M monthly downloads; MCP did it in 16 months.

Server ecosystem:
- Nov 2024: handful of experimental servers
- Apr 2025: ~100,000 server downloads/month
- Sept 2025: MCP Registry launched with ~2,000 entries, 407% increase from initial batch
- Nov 2025: 10,000+ active public servers
- Apr 2026: MCP directory lists 1,000+ standalone servers; 65% of tools on aggregator platforms wrap MCP servers

Community scale (as of Nov 2025): 58 maintainers, 9 core/lead maintainers, 2,900+ Discord contributors, 100+ new contributors weekly, 17 SEPs processed in ~one quarter.

GitHub metrics (spec repo `modelcontextprotocol/modelcontextprotocol`): 7.8k stars, 1.4k forks, 161 watchers, 136 open issues, 82 open PRs, 3,728 total commits, 7 releases. Servers reference repo: 79,017 stars.

Major adopters by timeline:
- Nov 2024: Anthropic Claude Desktop (initial)
- Mar 2025: OpenAI (ChatGPT desktop, API)
- Apr 2025: Google DeepMind
- Jul 2025: Microsoft (VS Code GitHub Copilot, Azure, Semantic Kernel)
- Nov 2025: AWS
- Active clients: Claude Desktop, Claude Code, Cursor, VS Code, ChatGPT, Gemini, Microsoft Copilot

**AAIF governance donation (December 9, 2025)**

Anthropic donated MCP to the Agentic AI Foundation (AAIF), a directed fund under the Linux Foundation. AAIF co-founded by Anthropic, Block, and OpenAI, with support from Google, Microsoft, AWS, Cloudflare, and Bloomberg. Founding projects: MCP (Anthropic), goose (Block), AGENTS.md (OpenAI).

Governance structure: The AAIF Governing Board handles strategic investment, budget, and member recruitment; individual projects retain full technical autonomy. MCP's existing governance model (maintainers + SEP process) remains unchanged. This moved MCP from a vendor-controlled project to a neutral steward with "decades of experience managing critical open-source projects."

TechCrunch: "OpenAI, Anthropic, and Block join new Linux Foundation effort to standardize the AI agent era."

---

### Sub-question 2: Server primitives and design principles

**Architecture layers**

MCP has two layers:

1. **Data layer** — JSON-RPC 2.0 based protocol defining lifecycle management and primitives (tools, resources, prompts, notifications, tasks). This is stateful by default; a stateless subset is available via Streamable HTTP.

2. **Transport layer** — communication mechanisms:
   - **stdio** — standard input/output streams; direct process communication for local integrations; optimal performance, no network overhead; a server runs as a subprocess of the host
   - **Streamable HTTP** — HTTP POST for client-to-server; optional Server-Sent Events for streaming. Supports OAuth 2.1 bearer tokens, API keys, custom headers. SSE was the previous remote transport (pre-2025-03-26 spec), now deprecated as standalone.

**Participants**

- **MCP Host**: The AI application (Claude Desktop, VS Code, Cursor, custom agent). Manages one or more clients.
- **MCP Client**: One per server connection. Maintains dedicated 1:1 connection. Handles capability negotiation.
- **MCP Server**: Exposes primitives. Runs locally (stdio subprocess) or remotely (Streamable HTTP).

Local servers typically serve a single client. Remote Streamable HTTP servers serve many clients.

**Connection lifecycle**

1. Client sends `initialize` request with `protocolVersion` and `capabilities`
2. Server responds with its `capabilities` and `serverInfo`
3. Client sends `notifications/initialized`
4. Active session: bidirectional requests/responses/notifications
5. Either party can close

**Server primitives (what servers expose to clients)**

*Tools* — executable functions the LLM can invoke:
- Described by `name` (canonical identifier, e.g. `weather_current`), `title` (human display), `description` (agent-facing usage guidance), `inputSchema` (JSON Schema), optional `outputSchema`
- Discovery: `tools/list`; execution: `tools/call`
- Servers can notify of changes via `notifications/tools/list_changed` if they declared `listChanged: true` in capabilities
- Tool names: guidance added in 2025-11-25; canonical format standardized across SDKs

*Resources* — data sources providing context (not actions):
- Examples: file contents, database records, API responses, schemas, configuration
- Discovery: `resources/list`; retrieval: `resources/read`
- Support URI templates for dynamic resources

*Prompts* — reusable interaction templates:
- Functions that generate messages or instructions, often parameterized
- Discovery: `prompts/list`; retrieval: `prompts/get`

**Client primitives (what clients expose to servers)**

- **Sampling** — servers can request LLM completions from the host via `sampling/createMessage`. Keeps servers model-agnostic. Added tool-calling support to sampling in 2025-11-25 (SEP-1577).
- **Elicitation** — servers request additional user input mid-session via `elicitation/create`. Introduced in 2025-06-18; URL mode added in 2025-11-25 (SEP-1036) for out-of-band credential flows via browser.
- **Roots** — servers can query filesystem/URI boundaries the host permits them to operate within.
- **Logging** — servers send log messages to clients.

**Cross-cutting utilities**

- **Tasks (experimental, SEP-1686)** — durable execution wrappers for long-running operations. States: `working`, `input_required`, `completed`, `failed`, `cancelled`. Call-now/fetch-later pattern via polling. Introduced in 2025-11-25.
- Progress tracking, cancellation, error reporting.
- Real-time notifications (JSON-RPC notifications without `id` field, no response expected).

**Design principles (derived from spec and architecture docs)**

1. LSP-inspired — standardizes context/tool integration across AI applications, analogous to Language Server Protocol's role for programming languages
2. Stateful connections by default — capability negotiation on connect; stateless mode available via Streamable HTTP for horizontal scaling
3. Dynamic discovery — `*/list` methods allow capability listings to change at runtime
4. Separation of concerns — servers handle capability implementation, clients handle orchestration, hosts handle UX and consent
5. Security by design — "User Consent and Control" as first-listed key principle; tools treated as arbitrary code execution requiring explicit consent; "LLM Sampling Controls" requiring explicit user approval

---

### Sub-question 3: Building servers vs. consuming as client

**Python: FastMCP server pattern**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ServiceName", json_response=True)

@mcp.tool()
def search_tickets(query: str, status: str = "open") -> list[dict]:
    """Search by keyword returning ID, subject, status, assignee.
    Use 'status' to filter: open, closed, or pending. Max 25 results."""
    return [...]

@mcp.resource("scheme://resource/{id}")
def get_resource(id: str) -> str:
    return json.dumps({...})

@mcp.prompt()
def workflow_name(param: str) -> str:
    return f"Instructions for {param}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
    # OR: mcp.run()  # defaults to stdio
```

FastMCP uses Python type hints and docstrings to automatically generate tool definitions. The Python SDK is published as `mcp` on PyPI.

**TypeScript: McpServer + Zod pattern**

```typescript
import { McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";

const server = new McpServer({ name: "service", version: "1.0.0" });

server.registerTool(
  "tool-name",
  {
    title: "Display Name",
    description: "When/how agents use this...",
    inputSchema: z.object({ param: z.string() }),
    outputSchema: z.object({ result: z.string() })
  },
  async ({ param }) => ({
    content: [{ type: "text", text: JSON.stringify(data) }]
  })
);
```

The TypeScript SDK is published as `@modelcontextprotocol/sdk`. Framework integrations: `@modelcontextprotocol/express`, `@modelcontextprotocol/hono`. Additional community SDKs: C#, Java, Kotlin, Go, PHP, Perl, Ruby, Rust, Swift.

**Transport selection**

| Requirement | stdio | Streamable HTTP |
|---|---|---|
| Desktop tools (Claude, VS Code, Cursor) | preferred | works with config |
| Local development | preferred | viable |
| Remote/cloud deployment | no | required |
| Multi-user access | no | yes |
| Authentication | none needed | OAuth 2.1 + PKCE |
| Serverless (Lambda, Vercel) | no | yes (stateless mode) |

stdio deployment: entry in Claude Desktop `claude_desktop_config.json`:
```json
{ "mcpServers": { "name": { "command": "python", "args": ["./server.py"] } } }
```

**Tool design best practices**

- Keep tool descriptions actionable for agents: specify what the tool does, when to invoke it, parameter constraints, return format, rate limits
- 5–10 focused tools per server preferred over 30+ monolithic services; compose via multiple servers
- Structured error responses enable agent self-correction (MCP 2025-06-18 codified this: input validation errors should return Tool Execution Errors, not Protocol Errors)
- Use `outputSchema` (added 2025-06-18 structured outputs) for typed response contracts

**Client consumption patterns**

Python client:
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(StdioServerParameters(command="python", args=["server.py"])) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        result = await session.call_tool("tool-name", arguments={...})
```

TypeScript client:
```typescript
const client = new Client({ name: "agent", version: "1.0.0" });
await client.connect(new StdioClientTransport({ command: "python", args: ["server.py"] }));
const tools = await client.listTools();
```

**Host implementations (major clients)**

- **Claude Desktop / Claude Code** — original MCP clients by Anthropic; support both stdio and remote; Claude Code can act as both MCP client AND server
- **Cursor** — most popular IDE client; stdio via `mcp.json`; drove protocol from chatbot feature to developer tool
- **VS Code / GitHub Copilot** — MCP support reached GA in VS Code 1.102 (July 2025); auto-discovers servers from other installed tools
- **ChatGPT** — requires OAuth 2.1 for remote MCP servers

**Production deployment patterns**

- Composition: one agent host connects to multiple focused MCP servers (CRM, billing, inventory, notifications)
- Stateless Streamable HTTP for horizontal scaling behind load balancers (Ray Serve, AWS Lambda, Vercel)
- Session management, rate limiting, DNS rebinding protection, strict CORS required for production
- OAuth 2.1 with `/.well-known/oauth-protected-resource` discovery for auth; integrates with Auth0, Okta, Azure AD

---

### Sub-question 4: MCP vs. alternative protocols

**MCP vs. function calling (OpenAI/Anthropic tool use)**

Function calling embeds tool definitions directly in LLM API requests. MCP uses a separate client-server architecture.

| Dimension | Function Calling | MCP |
|---|---|---|
| Implementation speed | Fast — no extra infrastructure | Slower — separate server process |
| Provider lock-in | Vendor-specific schemas | Provider-agnostic universal protocol |
| Modularity | Tools coupled to application | Tools reusable across clients and providers |
| Security | Credentials in main app | Isolated server-level credential management |
| Scalability | Tools compete for app resources | Independent scaling per server |
| Maintenance | Tool changes require app redeploy | Separate CI/CD per MCP server |

When to use function calling: proof-of-concept, single provider, handful of tools, speed-to-market priority.
When to use MCP: production deployment, multi-provider, shared tools across projects, enterprise security requirements, scaling from experimental to production.

The article from Descope characterizes MCP as "the natural evolution," comparing it to "USB-C port for AI applications." Zilliz frames it as reducing M×N integration complexity to M+N by standardizing capability advertisement.

**MCP vs. LangChain tools / Semantic Kernel plugins**

LangChain and LangGraph are development *frameworks* (orchestration, memory, chains), not protocols. They can integrate with MCP servers through adapters, treating them as tools. This is a hybrid: LangGraph provides agent orchestration while MCP servers handle standardized integrations.

Semantic Kernel is also a framework, not a protocol. Microsoft shipped first-class MCP support for Python in SK v1.28.1 — SK can now act as both MCP client and server natively. SK gains MCP's cross-platform interoperability; MCP servers gain SK's memory management.

Key distinction: MCP is a *protocol*, LangChain/SK are *frameworks*. They are complementary, not competing.

**MCP vs. A2A (Agent2Agent Protocol)**

A2A was launched by Google on April 9, 2025, with 50+ technology partners. On June 23, 2025, it was donated to the Linux Foundation as a separate standalone project (not part of AAIF; founding members: Google, AWS, Cisco, Microsoft, Salesforce, SAP, ServiceNow).

| Dimension | MCP | A2A |
|---|---|---|
| Scope | Agent-to-tool communication | Agent-to-agent communication |
| Focus | Providing tools, resources, context to an agent | Enabling agents to discover and delegate work to peer agents |
| Transport | stdio or Streamable HTTP | HTTP, SSE, JSON-RPC (same underlying stack) |
| Discovery | Tool/resource listing via `*/list` | "Agent Card" JSON format for capability advertisement |
| Relationship | Complementary — different layer | Complementary — different layer |

The official relationship: MCP provides tools and context *to* an agent; A2A enables agents to *collaborate with* other agents. Both operate on similar wire protocols (HTTP, JSON-RPC) but solve different interoperability problems. Google's announcement: "A2A complements Anthropic's Model Context Protocol (MCP)."

Recommended layering (Zilliz): use function calling for quick prototyping, MCP adapters for scalable tool ecosystems, A2A orchestration for multi-agent workflows.

---

### Sub-question 5: Limitations and roadmap

**Current security limitations**

MCP's core security problem: the protocol cannot enforce security at the protocol level — it relies on implementers following "SHOULD" requirements for user consent. Simon Willison (April 9, 2025): "Mixing tools with untrusted instructions is inherently dangerous."

Named attack classes:
1. **Tool poisoning** — malicious instructions embedded in tool descriptions, visible to LLMs but not users; can direct model to exfiltrate data or take unintended actions
2. **Indirect prompt injection** — malicious instructions in data accessed *through* MCP servers (files, emails, web content)
3. **Rug pull attacks** — legitimate-appearing tools become malicious after gaining user trust; tool definitions can mutate post-installation
4. **Tool shadowing** — malicious servers override or mimic trusted tools
5. **Data exfiltration via mixed tools** — Invariant Labs demonstrated a fake "get_fact_of_the_day" tool redirecting WhatsApp messages to an attacker; WhatsApp MCP was legitimate, the second server weaponized it
6. **CVE-2025-6514** (JFrog) — critical OS command-injection in `mcp-remote` (popular OAuth proxy); malicious servers could send a booby-trapped `authorization_endpoint` achieving RCE on the client machine

Empirical findings (March 2025 researcher analysis): 43% of tested MCP server implementations contained command injection flaws; 30% permitted unrestricted URL fetching; 22% had path traversal vulnerabilities; 492 public servers identified as vulnerable to abuse.

Willison's prescriptions: clients should display tool descriptions initially and alert users when descriptions change; treat spec "SHOULD" requirements for human oversight as "MUST."

**Current production operational limitations**

1. **Stateful session management at scale** — Streamable HTTP's default statefulness creates problems behind load balancers; stateless mode is a workaround, not yet fully specified
2. **Configuration fragmentation** — each MCP host (Claude, Cursor, VS Code, ChatGPT) has a different config format; the #1 pain point for teams supporting multiple clients
3. **OAuth complexity** — OAuth 2.1 is required but often skipped or poorly implemented in public servers; 2025-11-25 simplified registration with Client ID Metadata Documents but the auth path remains complex
4. **No audit trail standard** — enterprises need end-to-end visibility into what agent requested and what server executed; no standard currently
5. **Gateway/proxy behavior undefined** — behavior when a client routes through an intermediary is not yet specified in core
6. **Tasks primitive is experimental** — SEP-1686 Tasks (async workflows) landed in 2025-11-25 as experimental; retry semantics and result expiry policies are known gaps

**Spec version history gaps**

- JSON-RPC batching was *removed* in 2025-06-18 — a breaking change for implementations that relied on it
- SSE standalone transport deprecated in 2025-03-26 in favor of Streamable HTTP; older servers still run SSE for backward compatibility
- No Python-equivalent of FastMCP in official TypeScript SDK initially (third-party pattern)

**2026 Official Roadmap (last updated 2026-03-05)**

Four strategic priority areas:

1. **Transport Evolution and Scalability**
   - Next-generation Streamable HTTP: stateless operation across multiple instances, correct behavior behind load balancers/proxies
   - Scalable session handling: session creation, resumption, migration protocol
   - MCP Server Cards: `.well-known` URL exposing structured server metadata for discovery by browsers, crawlers, registries — without connecting
   - Owned by Transports WG and Server Card WG
   - No additional transports planned this cycle

2. **Agent Communication**
   - Close gaps in Tasks primitive lifecycle: retry semantics, result expiry policies
   - Owned by Agents WG

3. **Governance Maturation**
   - Contributor ladder SEP: clear progression from community → WG contributor → WG facilitator → lead maintainer → core maintainer
   - Delegation model: trusted WGs can accept SEPs in their domain without full core-maintainer review
   - Charter template for every WG/IG, reviewed quarterly
   - Owned by Governance WG
   - Background: SEP-1302 formalized WGs/IGs; SEP-2085 established succession/amendment procedures

4. **Enterprise Readiness**
   - Audit trails and observability (for existing logging/compliance pipelines)
   - Enterprise-managed auth: paved paths to SSO-integrated flows (Cross-App Access / xaa.dev), away from static client secrets
   - Gateway and proxy behavior: auth propagation, session semantics, what intermediaries can see
   - Configuration portability: configure once, work across clients
   - Expected to form an Enterprise WG; output likely as extensions, not core spec

**On the Horizon (lower priority, community-driven)**

- Triggers and event-driven updates (server-initiated webhooks/callbacks, replacing polling/persistent SSE)
- Streamed and reference-based result types (incremental output; large-payload lazy pull)
- Finer-grained security: least-privilege scopes, DPoP (SEP-1932), Workload Identity Federation (SEP-1933), community vulnerability disclosure via Linux Foundation
- Extensions ecosystem maturation: maturing `ext-auth` and `ext-apps` tracks; possible Skills primitive for composed capabilities; first-class extension support in registry
- Conformance test suites and SDK tiering (SEP-1730) as ongoing validation investments

**SEP velocity insight**

SEPs aligned with the four priority areas receive expedited review. SEPs outside these areas face longer timelines and higher justification bar. Maintainer capacity is explicitly finite and publicly disclosed as directing to these priorities first. This transparency about bandwidth allocation is a new governance practice introduced with the 2026 roadmap.

---

## Key Takeaways

**Bottom line:** MCP is the de facto standard for agent-tool integration as of early 2026. With 97M monthly SDK downloads, 10,000+ servers, and backing from Anthropic, OpenAI, Google, Microsoft, and AWS under Linux Foundation neutral governance, the ecosystem consolidation is largely complete.

**What it is:** A JSON-RPC 2.0 protocol (inspired by Language Server Protocol) connecting AI hosts to tool servers through three primitives: Tools (actions), Resources (context data), Prompts (reusable templates). Two transports: stdio (local) and Streamable HTTP (remote).

**What it solves vs. alternatives:** MCP reduces M×N tool-integration complexity to M+N by standardizing capability advertisement. Function calling is simpler but vendor-specific. LangChain/Semantic Kernel are frameworks that can *consume* MCP servers. A2A is complementary — where MCP is agent-to-tool, A2A is agent-to-agent.

**Where it struggles:** Security is the acute gap — tool poisoning, prompt injection, and rug pull attacks are inherent risks when LLMs process untrusted data alongside tools. The protocol cannot enforce consent at the wire level. Production scaling via stateless Streamable HTTP is viable but under-specified. Enterprise auth, audit, and gateway behavior are known gaps with active 2026 roadmap attention.

**Where it's heading:** Transport scalability (stateless HTTP, Server Cards for discovery), Tasks primitive hardening, governance delegation, and enterprise readiness (audit trails, SSO, gateway patterns). Next spec release tentatively June 2026.

---

## Findings

### MCP is the dominant open standard for agent-tool connectivity, with explosive but uneven adoption

MCP launched November 25, 2024 and grew from ~2M/month SDK downloads to a widely-cited figure of 97M/month by March 2026 (combined Python + TypeScript SDKs; see Challenge for caveats). 10,000+ public server implementations exist by third-party counts, though the official registry shows ~2,000 [1][13]. The protocol was donated to the Linux Foundation AAIF on December 9, 2025 alongside AGENTS.md — governance is now vendor-neutral. HIGH confidence for rapid adoption trajectory; MODERATE confidence for specific statistics.

### Three server primitives: Tools (agent-controlled), Resources (app-controlled), Prompts (user-controlled)

MCP cleanly separates what the model controls (tool invocations), what the host app controls (resource access), and what the user controls (prompt templates) [1][2][3]. This taxonomy maps cleanly onto authorization: resources can be read-only, tools require explicit permission grants. Tools now support `outputSchema` for validated structured results and four `annotations` boolean hints (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) added March 2025. HIGH confidence (T1 spec sources).

### Two transport mechanisms: stdio for local, Streamable HTTP for remote

stdio (client spawns server as subprocess, communicates via stdin/stdout) is the standard for desktop tools and local development. Streamable HTTP (POST + optional SSE, with `Mcp-Session-Id` header) replaced the 2024-era HTTP+SSE in the March 2026 spec and is the path for production remote servers [1][2]. Stateless Streamable HTTP for horizontal scaling is on the roadmap but not yet standardized — avoid presenting it as production-ready. HIGH confidence.

### MCP solves M×N → M+N: one server serves many clients, any framework

Unlike function calling (tools redefined per request, per vendor), MCP tools are defined once and discoverable at runtime via `tools/list`. Any MCP-compatible client can connect to any MCP server without modification. Semantic Kernel, LangChain, LlamaIndex all have MCP client support [9][10][11]. Function calling remains faster-to-start for single-model internal tools; MCP wins for shared integrations across teams and models. HIGH confidence.

### MCP has real security vulnerabilities: tool poisoning, prompt injection, and a critical RCE (CVE-2025-6514)

CVE-2025-6514 (CVSS 9.6, July 2025): mcp-remote versions 0.0.5–0.1.15 had an RCE vulnerability fixed in 0.1.16 [14]. Tool poisoning (malicious servers embedding hidden instructions in tool descriptions) and indirect prompt injection are unmitigated at the protocol level — annotations are hints, not security guarantees. Enterprise deployments require network controls and sandboxing beyond what MCP provides. HIGH confidence for CVE; MODERATE for broader prevalence (see Challenge on the 43% injection statistic).

### Key canonical tools and references

- **MCP spec (current):** https://modelcontextprotocol.io/specification/2025-11-25/ — tools, resources, prompts, transports
- **Python FastMCP:** https://github.com/modelcontextprotocol/python-sdk — `@mcp.tool()` decorator pattern
- **MCP TypeScript SDK:** https://github.com/modelcontextprotocol/typescript-sdk — `server.tool()` with Zod
- **AAIF announcement:** https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation — governance structure
- **MCP anniversary post:** https://modelcontextprotocol.io/blog/anniversary — adoption data with source caveats

## Challenge

### Claim-by-Claim Strength Assessment

**1. "97M/month npm downloads by March 2026" — MODERATE**

The 97M figure is widely cited across secondary sources (bitcoin.com, DEV Community, DigitalApplied) and attributed to Anthropic. However:

- The original primary source is not a verifiable public data point. The MCP anniversary blog post (Nov 2025) does not mention this figure — it cites ~2,000 registry entries and community metrics. The number appears to trace to an Anthropic announcement or press statement, not directly to npm/PyPI download dashboards.
- The document states these are "combined Python+TypeScript" SDK downloads, which is accurate per secondary sources — but this aggregation is rarely stated explicitly; many citations treat it as a single-package figure.
- npm counts package downloads including CI pipelines, automated scripts, and mirror re-downloads. This is standard npm methodology but inflates the signal vs. unique users or active deployments. The comparison to React (which faces the same inflation) is fair, but neither figure measures actual production usage.
- No independent raw npm or PyPI data point corroborates the 97M number. The figure is **unverified via primary registry data**.

**2. "10,000+ public MCP servers" — LOW**

This claim has significant measurement problems:

- The MCP official anniversary blog (Nov 2025, the document's own T1 source) reports ~2,000 registry entries — not 10,000+. The document cites this same blog as source 5 but attributes a 10,000 figure to "Nov 2025."
- Third-party aggregators (PulseMCP, SkillsIndex, FastMCP, PopularAiTools) report wildly divergent counts: 1,864 (FastMCP), 4,133 (SkillsIndex), 8,600+ (SkillsIndex "all public registries"), 11,130+ (PulseMCP), 12,000+ (PopularAiTools). These use incompatible methodologies with no disclosed quality thresholds. PulseMCP explicitly "omits low quality implementations" but does not state its criteria.
- "Public" is undefined across sources. It may mean: (a) listed in a public registry, (b) accessible over the internet, (c) open-source on GitHub, or (d) some combination. Most remote/HTTP MCP servers require authentication and are not freely accessible.
- The 10,000 figure appears to originate from secondary commentary, not the official MCP registry. **Flag as unverified.** The defensible figure from T1 sources is ~2,000 registry entries as of Nov 2025.

**3. "43% of tested MCP servers had command injection flaws" — LOW**

This is the weakest statistical claim in the document:

- The source is an Equixly blog post (March 29, 2025) by the company's CTO. It is not a peer-reviewed study, not a formal security audit with disclosed methodology, and not associated with an academic or recognized security research institution.
- Equixly does not disclose the sample size, selection criteria, testing tools, or timeframe. The post says "the past weeks deep diving into some R&D."
- The companion statistics (30% unrestricted URL fetching, 22% path traversal, 492 vulnerable servers) are also undisclosed-methodology figures from the same source.
- The document attributes this to "March 2025 researcher analysis" — accurate in that it was published in March 2025, but "researcher analysis" implies more rigor than a vendor blog post without disclosed methodology.
- The Equixly post references a separate independent finding from a single researcher (@junr0n) but does not cite them as the source of the 43% figure. **Flag as unverified; origin is a single undisclosed-methodology vendor blog.**

**4. "CVE-2025-6514 (mcp-remote RCE)" — HIGH**

This claim is accurate and well-supported:

- CVE-2025-6514 is a real, assigned CVE listed in NVD and the GitHub Advisory Database (GHSA-6xpm-ggf7-wc3p).
- Discovered and disclosed by JFrog Security Research on July 9, 2025. CVSS score: 9.6 (Critical).
- The affected package is `mcp-remote` (versions 0.0.5–0.1.15), an OAuth proxy that enables stdio-only LLM hosts to connect to remote MCP servers.
- Attack vector: malicious server returns a crafted `authorization_endpoint` URL that triggers OS command injection via the browser-open call. Fixed in version 0.1.16.
- No material discrepancies found. The document accurately describes the mechanism.

**5. "A2A protocol now also under Linux Foundation" / "In February 2026 it was donated to Linux Foundation" — FAIL**

The document's stated date is wrong, and the governance framing is imprecise:

- A2A was donated to the Linux Foundation on **June 23, 2025** — announced at Open Source Summit North America. The founding members were Google, AWS, Cisco, Microsoft, Salesforce, SAP, and ServiceNow. The "February 2026" date in the document has no supporting evidence and does not match any verifiable announcement.
- A2A is a **separate Linux Foundation project**, independent of the AAIF (Agentic AI Foundation) that houses MCP. The document's phrasing "also under Linux Foundation" is technically true (both LF) but implies a shared governance structure that does not exist. AAIF is a directed fund under LF; A2A is a standalone LF project.
- The document's Key Takeaways section claims "backing from Anthropic, OpenAI, Google, Microsoft, and AWS under Linux Foundation neutral governance" — this conflates AAIF (MCP's home) and the A2A project. MCP's governance is via AAIF; A2A's founding members include Google, AWS, Microsoft but A2A is not part of AAIF.

**6. "Stateless Streamable HTTP for horizontal scaling" — MODERATE (framing is misleading)**

The document describes stateless Streamable HTTP as a working production pattern. The official MCP transport post (Dec 19, 2025) contradicts this framing:

- The Dec 2025 MCP blog explicitly describes stateless mode as **not yet standardized**: "Many SDKs already offer a stateless option in their server transport configuration, though the behavior varies across implementations." The roadmap commits to standardizing what "stateless" means across SDKs — meaning it is not currently consistent.
- The post uses exploratory language throughout: "We are exploring," "We envision," "We're looking at." These are proposals, not shipped features.
- The Transport WG roadmap targets finalizing stateless semantics for the **June 2026 spec release** — meaning it was not finalized as of the document's research date (April 2026).
- The document's own roadmap section (Sub-question 5) correctly identifies "Stateful session management at scale" as a current limitation and "stateless mode is a workaround, not yet fully specified." The Key Takeaways and Sub-question 3 production patterns section contradicts this by presenting stateless deployment as viable today.
- The description "serverless-compatible" is accurate for many use cases, but the assertion that stateless Streamable HTTP is production-ready for horizontal scaling behind load balancers overstates current spec completeness.

**7. "MCP launched November 2024, spec version 2024-11-05" — HIGH**

This is accurate with one minor ambiguity:

- MCP was publicly announced by Anthropic on November 25, 2024. The initial spec version identifier is `2024-11-05` — the November 5 date in the identifier predates the public announcement by ~20 days, consistent with an internal freeze date before public release.
- The document correctly states both the public announcement date (Nov 25, 2024) and the spec version identifier (`2024-11-05`). No discrepancy found.

---

### Statistics That Could Not Be Independently Corroborated

| Claim | Status | Issue |
|---|---|---|
| 97M monthly SDK downloads (Mar 2026) | Unverified via primary registry data | Traces to Anthropic announcements; no raw npm/PyPI data published |
| 10,000+ active public servers (Nov 2025) | Contradicted by T1 source | MCP anniversary blog cites ~2,000; third-party counts range 1,864–12,000+ with incompatible methods |
| 43% of tested MCP servers had command injection | Unverified | Single undisclosed-methodology vendor blog; no sample size, no peer review |
| 30% unrestricted URL fetching, 22% path traversal, 492 vulnerable servers | Unverified | Same Equixly source as above |
| A2A donated to Linux Foundation "February 2026" | Factually wrong | Actual date: June 23, 2025 |

---

### What This Research Does Not Cover

- **Raw SDK download data.** No direct npm or PyPI registry query was performed. All download statistics are secondary claims traceable to Anthropic without independent confirmation.
- **Actual MCP server registry enumeration.** No query against the official MCP registry was performed; server counts are entirely from third-party aggregators with opaque methodology.
- **The MCP Registry itself.** The registry (launched ~Sept 2025) is mentioned but its discoverability, submission standards, and quality criteria are not examined. It may be the best single source for server counts.
- **Enterprise adoption depth vs. breadth.** The document covers which companies adopted MCP but not how deeply (number of servers in production, traffic volumes, incident rates).
- **SDK version fragmentation.** Multiple spec versions (2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25) coexist; no analysis of which spec versions the installed SDK base actually implements.
- **Non-TypeScript/Python SDKs.** Community SDKs (C#, Go, Rust, Java, etc.) are mentioned but not assessed for completeness, maintenance status, or spec conformance.
- **The security vendor landscape.** The security section relies on a small number of sources (Simon Willison, Equixly, Prompt Security, JFrog). Systematic security research from academic or government sources was not found.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | MCP launched November 25, 2024; initial spec version is `2024-11-05` | Factual — date and identifier | [5] anniversary blog, [1] spec | Verified — announcement date and spec version identifier both confirmed by T1 sources |
| 2 | 97M/month SDK downloads by March 2026 (combined Python + TypeScript) | Statistic — adoption scale | Secondary sources attribute to Anthropic announcement; not in [5] anniversary blog | Needs human review — no primary npm/PyPI data; Challenge confirms figure traces to Anthropic press statements only |
| 3 | 10,000+ active public MCP servers as of November 2025 | Statistic — ecosystem size | [5] T1 anniversary blog contradicts: cites ~2,000 registry entries | Corrected — T1 source ([5]) says ~2,000 registry entries; 10,000+ figure is third-party aggregator data with inconsistent methodology |
| 4 | MCP donated to Linux Foundation AAIF on December 9, 2025 | Factual — governance event | [7] Anthropic announcement, [8] Linux Foundation press release | Verified — both T1 sources confirm date, co-founders (Anthropic, Block, OpenAI), and directed-fund structure |
| 5 | AAIF co-founded by Anthropic, Block, and OpenAI with Google, Microsoft, AWS, Cloudflare, Bloomberg as supporters | Factual — governance membership | [7], [8] | Verified — confirmed by T1 primary sources |
| 6 | A2A protocol donated to Linux Foundation on June 23, 2025 (not February 2026) | Factual — governance date | [11] Google A2A announcement; Challenge section correction | Corrected — document originally stated "February 2026"; correct date is June 23, 2025 per Challenge analysis; A2A is a separate LF project, not part of AAIF |
| 7 | Three server primitives: Tools (agent-controlled), Resources (app-controlled), Prompts (user-controlled) | Architectural — core model | [1] spec, [2] architecture, [3] changelog | Verified — T1 spec sources confirm primitive taxonomy and control model |
| 8 | Streamable HTTP replaced standalone SSE in the March 2025 spec (2025-03-26); SSE deprecated | Factual — spec history | [1] spec, [3] changelog | Verified — T1 spec and changelog confirm deprecation timing |
| 9 | CVE-2025-6514: mcp-remote OS command injection RCE, CVSS 9.6, fixed in version 0.1.16 (July 2025) | Security — CVE | External: NVD, GHSA-6xpm-ggf7-wc3p, [14] JFrog; confirmed in Challenge | Verified — CVE is real, CVSS 9.6, mechanism and fix version confirmed by Challenge analysis |
| 10 | 43% of tested MCP server implementations had command injection flaws (March 2025) | Statistic — security prevalence | [14] single vendor blog (Equixly); no disclosed sample size or methodology | Needs human review — Challenge flags as weakest statistical claim: single undisclosed-methodology vendor blog, no sample size, no peer review |
| 11 | 30% of servers permitted unrestricted URL fetching; 22% had path traversal; 492 servers vulnerable to abuse | Statistics — security prevalence | Same Equixly source as claim 10 | Needs human review — same source and methodology problems as claim 10; all four figures are from a single undisclosed vendor analysis |
| 12 | Semantic Kernel v1.28.1 shipped first-class MCP support; SK can now act as both MCP client and server | Factual — ecosystem integration | [12] Zilliz T3, no T1 Microsoft source cited | Needs human review — no T1 Microsoft or SK release notes source cited; T3 only |
| 13 | VS Code MCP support reached GA in VS Code 1.102 (July 2025) | Factual — client milestone | [16] Particula Tech T3; no T1 Microsoft source cited | Needs human review — T3 source only; no official VS Code release notes or Microsoft blog cited |
| 14 | Stateless Streamable HTTP enables production horizontal scaling behind load balancers | Architectural — deployment claim | [4] roadmap (T1); Challenge contradicts: roadmap describes this as not yet standardized | Corrected — Challenge analysis confirms stateless mode behavior varies across SDKs and standardization targets June 2026 spec; presenting as production-ready overstates current spec completeness |
| 15 | JSON-RPC batching was removed in the 2025-06-18 spec (breaking change) | Factual — spec history | [1] spec, [3] changelog, [17] ForgeCode T3 | Verified — T1 spec changelog confirms removal of JSON-RPC batching as a deliberate breaking change in 2025-06-18 |
