# mai-analysis
Learning player skill representations for personalized chart recommendation in maimai DX.、

## Overview

**mai-analysis** is an open-source research project that aims to model player abilities from large-scale real maimai DX score data.

Instead of recommending charts solely based on difficulty constants, this project learns latent relationships between **players** and **charts**, enabling personalized chart recommendation and chart similarity analysis.

---

## Motivation

Current chart recommendations are usually based on:

- Difficulty constant
- Rating
- Community experience

However, charts with the same difficulty often require very different skills.
~~致敬传奇13.6太空哈利~~

For example, two level 14 charts may emphasize completely different abilities such as:

- Touch patterns
- Star handling
- Slide techniques
- Rhythm complexity

This project aims to automatically discover these latent skill requirements from player score data.
