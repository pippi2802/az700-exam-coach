# AZ-700 Practice Quiz — ExpressRoute

- **Domain:** D2 — Design, implement, and manage connectivity services
- **Topic focus:** Azure ExpressRoute
- **Questions:** 5 (scenario-weighted)
- **Difficulty mix:** 1 easy · 2 medium · 1 hard · 1 exam-like
- **Generated:** 2026-06-30

> Answer the questions first. The **Answer key** with full explanations is in a
> separate section at the very end — scroll only when you are ready.

---

## Question 1

- **Domain:** D2
- **Subtopic:** ExpressRoute SKU and tier
- **Type:** scenario_design
- **Difficulty:** easy
- **Skill tested:** Choosing the correct ExpressRoute circuit SKU for a connectivity requirement.

**Scenario:** Contoso has an ExpressRoute circuit terminating in the West Europe
peering location. They have virtual networks in West Europe, East US, and
Southeast Asia and want a single ExpressRoute circuit to connect to virtual
networks in **all** of those regions across the globe.

**Question:** Which ExpressRoute circuit SKU should Contoso use?

- **A.** Local SKU
- **B.** Standard SKU
- **C.** Premium SKU
- **D.** ExpressRoute Direct only

---

## Question 2

- **Domain:** D2
- **Subtopic:** ExpressRoute Global Reach
- **Type:** scenario_design
- **Difficulty:** medium
- **Skill tested:** Selecting the feature that connects on-premises sites to each other over the Microsoft backbone.

**Scenario:** Fabrikam has two datacentres, one in London and one in Singapore.
Each datacentre already has its own ExpressRoute circuit into Azure for workload
connectivity. Fabrikam now wants the **London and Singapore datacentres to
communicate with each other** privately, routing traffic over the Microsoft
global network instead of the public internet, without deploying any VPN
gateways.

**Question:** Which capability should you configure?

- **A.** ExpressRoute FastPath
- **B.** ExpressRoute Global Reach
- **C.** ExpressRoute Direct
- **D.** Site-to-site VPN as a failover path

---

## Question 3

- **Domain:** D2
- **Subtopic:** ExpressRoute FastPath
- **Type:** scenario_design
- **Difficulty:** medium
- **Skill tested:** Identifying how to reduce data-path latency between on-premises and Azure VMs.

**Scenario:** Adatum runs latency-sensitive virtual machines in a hub virtual
network reached through an ExpressRoute circuit. Network monitoring shows that
the ExpressRoute **virtual network gateway** is a bottleneck on the data path
between on-premises servers and the VMs. Adatum wants traffic to bypass the
gateway in the data path while keeping the gateway for route exchange.

**Question:** What should you enable, and what is a key prerequisite?

- **A.** Enable FastPath; the gateway must be an Ultra Performance or ErGw3AZ SKU.
- **B.** Enable Global Reach; the gateway must be a Standard SKU.
- **C.** Enable BFD; the gateway must be a Basic SKU.
- **D.** Enable FastPath; the circuit must use the Local SKU.

---

## Question 4

- **Domain:** D2
- **Subtopic:** Private peering vs Microsoft peering
- **Type:** troubleshooting
- **Difficulty:** hard
- **Skill tested:** Mapping ExpressRoute peering types to the resources they reach.

**Scenario:** Northwind connects to Azure over ExpressRoute. Virtual machines in
their virtual networks are reachable over the circuit, but an application team
reports they **cannot reach the public endpoints of Azure PaaS services**
(for example, a storage account public endpoint and Microsoft 365) over the same
ExpressRoute circuit. Private peering is configured and healthy.

**Question:** What is the most likely cause and the correct remediation?

- **A.** Private peering does not carry public service traffic; configure
  Microsoft peering on the circuit.
- **B.** The circuit SKU is too low; upgrade from Premium to ExpressRoute Direct.
- **C.** FastPath is disabled; enable FastPath to expose public endpoints.
- **D.** Global Reach is required to reach Azure PaaS public endpoints.

---

## Question 5

- **Domain:** D2
- **Subtopic:** Encryption over ExpressRoute / ExpressRoute Direct
- **Type:** scenario_design
- **Difficulty:** exam_like
- **Skill tested:** Selecting an encryption approach for ExpressRoute that meets a layer-2/MACsec requirement.

**Scenario:** A regulated bank requires that all traffic traversing its
ExpressRoute connection be **encrypted at the link layer (Layer 2)** between its
edge routers and Microsoft's routers. They are provisioning **ExpressRoute
Direct** with dedicated ports and want native encryption on those ports rather
than running an IPsec tunnel over the circuit.

**Question:** Which encryption option meets the requirement?

- **A.** MACsec on the ExpressRoute Direct ports
- **B.** IPsec site-to-site VPN over Microsoft peering
- **C.** TLS termination at Azure Front Door
- **D.** Azure Firewall premium TLS inspection

---

# Answer key

> Spoilers below. Each item gives the correct answer, why it is correct, and why
> each distractor is wrong.

## Q1 — Correct: **C. Premium SKU**

The **Premium** add-on/SKU is what enables an ExpressRoute circuit to connect to
virtual networks **outside the circuit's own geopolitical region** (global
connectivity), and it raises route and VNet-link limits.

- **A. Local SKU** — wrong: Local is restricted to Azure regions in or near the
  circuit's own peering-location metro; it cannot reach VNets across the globe.
- **B. Standard SKU** — wrong: Standard allows connectivity to VNets within the
  same geopolitical region only, not globally.
- **D. ExpressRoute Direct only** — wrong: ExpressRoute Direct is about how you
  physically connect (dedicated ports at high bandwidth); it does not by itself
  grant cross-region VNet reachability — that is the Premium capability.

## Q2 — Correct: **B. ExpressRoute Global Reach**

**Global Reach** links ExpressRoute circuits together so your **on-premises
networks can exchange traffic with each other** through the Microsoft global
backbone — exactly the branch-to-branch (London ↔ Singapore) requirement.

- **A. FastPath** — wrong: FastPath optimises the on-premises-to-VM data path by
  bypassing the VNet gateway; it does not interconnect two on-premises sites.
- **C. ExpressRoute Direct** — wrong: Direct provides dedicated high-bandwidth
  ports into Microsoft's network; it is not a site-to-site interconnect feature.
- **D. Site-to-site VPN** — wrong: the requirement explicitly excludes VPN
  gateways and wants traffic on the Microsoft backbone, which Global Reach
  provides natively.

## Q3 — Correct: **A. Enable FastPath; gateway must be Ultra Performance or ErGw3AZ**

**FastPath** improves the data path by sending traffic **directly to/from VMs and
bypassing the ExpressRoute gateway**. It still requires a gateway for route
exchange, and it requires a high-tier gateway SKU — **Ultra Performance** or
**ErGw3AZ**.

- **B. Global Reach / Standard** — wrong: Global Reach connects on-premises sites,
  not a gateway-bypass feature; Standard gateway does not enable FastPath.
- **C. BFD / Basic** — wrong: BFD speeds up link-failure detection; it does not
  bypass the gateway, and Basic gateway is not valid for this.
- **D. FastPath / Local SKU** — wrong: the prerequisite is the **gateway** SKU,
  not the circuit's Local SKU; Local SKU is unrelated to FastPath enablement.

## Q4 — Correct: **A. Configure Microsoft peering**

ExpressRoute **private peering** carries traffic to private IP space in your
virtual networks. Reaching **public endpoints** of Azure PaaS services and
Microsoft 365 over ExpressRoute requires **Microsoft peering**, a separate
routing domain on the circuit.

- **B. Upgrade to ExpressRoute Direct** — wrong: peering type, not bandwidth/port
  model, is the issue; Direct does not add public-endpoint reachability.
- **C. Enable FastPath** — wrong: FastPath optimises the private data path to VMs;
  it does not expose public service endpoints.
- **D. Global Reach** — wrong: Global Reach interconnects on-premises sites; it
  has nothing to do with reaching Azure PaaS public endpoints.

## Q5 — Correct: **A. MACsec on the ExpressRoute Direct ports**

**MACsec** provides **Layer 2 (link-layer) encryption** on **ExpressRoute Direct**
ports between your routers and Microsoft's routers — matching the explicit
Layer-2 / native-port-encryption requirement.

- **B. IPsec over Microsoft peering** — wrong: IPsec is a Layer 3 option and runs
  *over* the circuit rather than encrypting the Direct ports at Layer 2; the bank
  specifically wants native port encryption, not a tunnel.
- **C. TLS at Front Door** — wrong: application-layer TLS for web traffic; not
  link-layer encryption of an ExpressRoute connection.
- **D. Azure Firewall TLS inspection** — wrong: inspects application traffic; it
  is not an ExpressRoute link-layer encryption mechanism.

---

## Sources used

- Microsoft Learn — Azure ExpressRoute documentation (circuits, SKUs/tiers,
  peering, Global Reach, FastPath, ExpressRoute Direct, MACsec encryption) — Tier 1.
- Microsoft Learn — Official AZ-700 study guide (Domain 2: connectivity services) — Tier 1.

> Verify any CLI/portal steps and current SKU/feature limits against Microsoft
> Learn before relying on them in production.
