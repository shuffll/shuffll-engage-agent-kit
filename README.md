# Shuffll Engage â€” Personalized video at scale

Create personalized video campaigns based on customer interests, behaviors, and audience segments. Tailor content across customer journeys, including e-commerce and product videos, and integrate it into your existing workflows through a robust API and MCP.

This repository distributes an agent skill and client connection packages. **Available features depend on your workspace, permissions and the live MCP tool catalog.** The skill checks those capabilities before acting. The legacy fixed-video campaign route does not personalize rendered media from recipient fields; message generation and delivery are separate operations. A source package does not establish approval by a client marketplace.

## Install the portable skill

```sh
npx skills add shuffll/shuffll-engage-agent-kit --skill shuffll-engage
```

Choose the agents and installation scope in the installer. The shared `SKILL.md` format is usable by supporting clients such as Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI and Windsurf. This installs instructions; configure and authenticate the MCP separately if your client does not consume the bundled connection. Individual client authentication and tool-call testing remain separate from skill installation.

## Claude Code plugin

```text
/plugin marketplace add shuffll/shuffll-engage-agent-kit
/plugin install shuffll-engage@shuffll-engage
```

This is a repository marketplace, separate from the Claude connector directory or the official Claude Code plugin catalog.

## Gemini CLI extension

```sh
gemini extensions install https://github.com/shuffll/shuffll-engage-agent-kit
```

The root manifest bundles the hosted MCP connection, and `skills/` contains the workflow guidance. An available repository does not prove gallery indexing or authenticated operation.

## GitHub Copilot plugin

```sh
copilot plugin marketplace add shuffll/shuffll-engage-agent-kit
copilot plugin install shuffll-engage@shuffll-engage
```

The Copilot-specific legacy manifest in `.plugin/plugin.json` preserves version metadata and the MCP connection while the Google plugin uses its own minimal root manifest. Authenticated tool calls and inclusion in GitHub's curated catalog are separate checks.

## Google Antigravity plugin

```sh
agy plugin install https://github.com/shuffll/shuffll-engage-agent-kit
```

The root `plugin.json`, `mcp_config.json` and `skills/` follow the documented Antigravity plugin format. The connection uses its supported remote `serverUrl` field and dynamic OAuth registration. Authenticate the intended workspace in Antigravity before using the MCP. This provides a direct repository installation route; curated Marketplace approval and native authenticated operation are separate checks.

## Cursor

The root `.cursor-plugin/plugin.json` bundles `skills/` and `mcp.json`. Use the repository with Cursor's plugin workflow. Official Cursor Marketplace review and client authentication are separate verification steps.

## Codex and ChatGPT

The `.codex-plugin/plugin.json` package combines the MCP with the skill for local testing and public review preparation. Public directory installation requires OpenAI review and publication. The portable skill command above provides a separate direct installation route for supporting local agents.

## Connect

MCP endpoint (Streamable HTTP): `https://engage.shuffll.com/mcp`

REST base URL: `https://engage.shuffll.com/api` (append the documented `/v1/...` operation path).

A paid Shuffll subscription and organization-enabled API/MCP access are required. Use your client's supported OAuth flow and choose the intended organization and minimum required permissions. If your client's OAuth flow is unavailable, consult the [authentication guide](https://api-docs.shuffll.com/engage) and use private client credential settings for a dedicated organization-scoped Engage API key where supported. Never commit keys or put them in URLs. If no organization is eligible, contact your administrator; this package does not enable access or change policy.

## Try it

- Show my authorized organizations and available capabilities.
- List published templates and identify which can render.
- Help me make a video preview using the creative tools available to my workspace.
- Create a campaign from my selected ready template without starting generation.
- Check my campaign's generation jobs and return its available video results.

The skill distinguishes previews, queued generation, completed media, and delivery. It preserves paired actor video/audio, keeps music beneath speech, and uses only verified native transitions available to the actual connection.

[Documentation](https://api-docs.shuffll.com/engage) Â· [Website](https://engage.shuffll.com) Â· [Support](https://api-docs.shuffll.com/contact)

Service use is subject to your Shuffll agreement and applicable [terms](https://shuffll.com/terms/) and [privacy policy](https://shuffll.com/privacy-policy/).

## Package license

The published agent-kit files are distributed under the [MIT License](LICENSE). Shuffll service access and API/MCP usage remain subject to your Shuffll agreement and applicable service terms. This license does not include Shuffll application source or grant service access.

## Research working drafts

Isaac Gili, Founder of Shuffll, is developing two research working drafts on controlled product variants and vector-art attachment in video. Read the [drafts, evidence boundaries, and planned evaluations](research/video-personalization/README.md). These are early research documents; neither has been submitted to arXiv or peer reviewed.
