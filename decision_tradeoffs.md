## MacroCycle AI Agent – Design Trade offs Matrix

```mermaid
flowchart LR
    A[**Design Simplicity**] --- B[**Production Readiness**]

    subgraph Simple Choices
        S1(Streamlit<br/>Rapid prototyping, open, reproducible)
        S2(Replit Sandbox<br/>Instant, isolated experimentation)
        S3(GPT-5 API<br/>Stable reasoning, faster iteration)
        S4(US Macro Data<br/>Reliable, richly described)
        S5(Local JSON Caching<br/>Cost efficient)
        S6(Open Repository<br/>Transparency & reuse)
        S7(AI-Assisted Dev<br/>Fast co-creation)
    end

    subgraph Scalable Choices
        P1(API-first Architecture<br/>Higher concurrency)
        P2(In-house Infrastructure<br/>Security & control)
        P3(Open LLM Stack<br/>Customisable, lower cost)
        P4(Defra Data Ecosystem<br/>Policy alignment)
        P5(Live API Calls<br/>Real-time accuracy)
        P6(Restricted Deployment<br/>Data assurance)
        P7(Traditional Dev Teams<br/>Formal governance)
    end

    %% Connect trade-offs visually
    S1 --> P1
    S2 --> P2
    S3 --> P3
    S4 --> P4
    S5 --> P5
    S6 --> P6
    S7 --> P7
