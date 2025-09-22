# Module Overview

What does each one do?


- **ch00_data_toolbox**: Create some standard tools files files, python dictionaries, databases, and other basic programming objects.
- **ch01_rope_logic**: Defines what a Rope is and required format for groups names and individual names.
- **ch02_finance_logic**: Defines tools for financial allotment to ledgers.
- **ch03_group_logic**: Defines a voice, and its group memberships. Groups will be produced from memberships.
- **ch04_reason_logic**: Describes what a reason and a fact is; if the reasons match the facts, the Reason.status = True
- **ch05_plan_logic**: Defines PlanUnits. Plans are complicated. A plan can have sub plans, define itself as a task, define Awardees, assigned Labor, required Reasons, etc.
- **ch06_belief_logic**: A belief is a beliefunit, made of accounts and plans. All plans are connected to the central plan, which is given all the funds in a beliefunit.
- **ch07_timeline_logic**: Allows arbitrary calendars to be defined for each beliefunit with minimal configuration.
- **ch08_belief_atom_logic**: Defines the structure and behavior of beliefunit atoms, which are single units of beliefunit and plans used in a beliefunit.
- **ch10_pack_logic**: Manages the creation and organization of packs, which are collections of beliefunit atoms for building complex beliefunits.
- **ch11_bud_logic**: Defines a budget and the tools necessary to create one. Budges are created when a moment system decides to empower a beliefunit with funds that must be distributed
- **ch12_hub_toolbox**: These tools are used to handle complex operations involving belief files, will be deprecated.
- **ch13_belief_listen_logic**: These tools describe how one beliefunit listens to another
- **ch14_keep_logic**: Builds a simulation that describes how much credit a healer has earned 
- **ch15_moment_logic**: A MomentUnit is a Moment system with the basic requirements: common system of time, voice tranactions ledger, etc. Importantly a Moment system must know the state of a belief's beliefunit at any time in the past.
- **ch16_pidgin_logic**: A tool that translates words from outside language to inside language.
- **ch17_idea_logic**: idea bricks are tables of data that build moment systems and the beliefunits within them.
- **ch18_etl_toolbox**: All the tools used by WorldUnits to create MomentUnits.
- **ch19_kpi_toolbox**: ch18_etl_toolbox manages the base required data. This toolbox manages the analytics outcomes.
- **ch20_world_logic**: WorldUnits create and manage MomentUnits
- **ch21_lobby_logic**: Tools for comparing how changes can create different WorldUnits.
- **ch22_belief_viewer**: Tools for Visualizing BeliefUnits
- **ch98_docs_builder**: TODO replace me