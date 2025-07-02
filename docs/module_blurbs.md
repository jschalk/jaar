# Module Overview

What does each one do?

- **a00_data_toolbox**: Creates a set of tools for data manipulation and analysis.
- **a01_term_logic**: Defines the terms and plans used in the system for consistent understanding and processing.
- **a02_finance_logic**: Defines financial rules and calculations to ensure accurate financial operations.
- **a03_group_logic**: Defines accounts, account memberships, and groups. Groups will be produced from memberships.
- **a04_reason_logic**: Describes what a reason and a fact is; if the reasons match the facts, then a task can be kept.
- **a05_plan_logic**: A plan can be a task, and if its reasons match its facts, it should be kept.
- **a06_owner_logic**: A owner is a ownerget, made of accounts and plans. All plans are connected to the axiom plan, which is given all the funds in a ownerget.
- **a07_timeline_logic**: Allows arbitrary calendars to be defined for each ownerget with minimal configuration.
- **a08_owner_atom_logic**: Defines the structure and behavior of ownerget atoms, which are single units of ownerget and plans used in a ownerget.
- **a09_pack_logic**: Manages the creation and organization of packs, which are collections of ownerget atoms for building complex ownergets.
- **a10_owner_calc**: Expresses the calculations performed when a ownerget is "settled" to determine final amounts for each plan and account.
- **a11_bud_logic**: When a belief system decides to empower a ownerget the funds must be distributed
- **a12_hub_tools**: These tools are used to handle complex operations involving owner files, will be deprecated.
- **a13_owner_listen_logic**: These tools describe how one ownerget listens to another
- **a14_keep_logic**: Builds a simulation that describes how much credit a healer has earned 
- **a15_belief_logic**: A BeliefUnit is a Belief system with the basic requirements: common system of time, acct tranactions ledger, etc. Importantly a Belief system must know the state of a owner's ownerget at any time in the past. 
- **a16_pidgin_logic**: A tool that translates words from outside language to inside language.  
- **a17_idea_logic**: idea bricks are tables of data that build belief systems and the ownergets within them.
- **a18_etl_toolbox**: 
- **a19_world_logic**: *(description needed)*
- **a20_lobby_logic**: *(description needed)*