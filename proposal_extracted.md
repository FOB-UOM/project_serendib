# Extracted proposal sections (OCR)

Source: the proposal PDF included with this repository. Generated from `proposal_ocr.txt`.

## Executive summary

THE CASE FOR SOVEREIGN Al

01 THE MANDATE

To move beyond simple translation and capture
“epistemic context” —the specific reasoning,
regulatory, and cultural dynamics of Sri Lanka.
Global models fail to grasp our local reality.

03 THE METHOD

Utilizing a ‘Lean-Al’ framework that prioritizes
curation over raw computation. We leverage
student participation to solve the ‘Data Scarcity’
bottleneck, turning a cost center into an
educational opportunity.

02 THE SOLUTION

Constructing a high-quality ‘Instruction Dataset’
and a ‘Reference AI Model’ (Lanka-Instruct-vl).
We prioritize Data as the primary asset, with the
Model as the proof of concept.

04 THE OUTCOME

Enabling the University to lead the nation in
sovereign AI development, building upon the
foundational success of local efforts like
SinLLM.

Ai NotebookLM

## Objectives

A TWO-TIERED APPROACH

=

PRIMARY OBJECTIVE: THE ASSET SECONDARY OBJECTIVE: THE PROOF

|

The Sri Lankan Open Instruction Dataset | Lanka-Instruct-vl (Pilot Model)
|
|

¢ A lightweight, efficient Small Language
Model (SLM).

° Goal: To demonstrate the utility of the
dataset in a practical application.

¢ A rigorously curated, multi-turn dialogue
dataset.

¢ Focus Domains: O/L & A/L Education, SME
Business Regulations, and Local History.

Ai NotebookLM

## Methodology

PARTICIPATORY DATA CURATION

strategy: Raw Data
Human-in-the-Loop. Sources
We leverage the student
body to curate and verify
raw data.

oo

From Cost Center to
Education Center:
Instead of viewing data
cleaning as a tedious
cost, we frame it as skill
acquisition. Students gain
credits, badges, and tangible Golden
experience in Data Standard
Engineering. Dataset

Gamified
Verification
& Cleaning

Flywheel

Student
Crowd
Engine

Ai NotebookLM


===== PAGE 8/13 =====

METHODOLOGY PHASE II: THE ‘LEAN-Al’ TECHNICAL LAYER

Transfer Learning

LoRA Adapter
(Trainable Parameters)

Pre-Trained Low-Rank Adaptation
Base Model
(Frozen Weights)

LoRA Adapter
(Trainable Parameters)

Technique: LoRA & PEFT. Goal.

Resource Efficiency.

We avoid the massive cost of Updating only a small fraction of To create an adaptive layer that
pre-training from scratch. Instead, parameters allows us to adapt the bridges the global base model
we utilize Transfer Learning. model to local contexts without high with local instruction data.

compute costs. This enables
operations on standard hardware.

Ai NotebookLM


===== PAGE 9/13 =====

METHODOLOGY PHASE III:
EVALUATION & DEPLOYMENT

|

Global Benchmarks (MMLU)

Redefining Success:
Cultural Benchmarking.

Success is not defined by beating
Google on general knowledge, but
by proving the dataset improves
local relevance.

The Test:

The model is tested against a
specifically created ‘Sri Lankan
Cultural Evaluation Set’.

Project Serendib
Target

Cultural Relevance

Deployment strategy:

A focus on lightweight deployment
allows the model to be accessible
to local researchers and
developers, ensuring the tool
remains usable within the
university ecosystem.

Ai NotebookLM
