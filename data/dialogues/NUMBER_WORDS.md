# Number words used in the dialogues (how the expected values were derived)

| Applicant writes | Value (IQD or months) |
|---|---|
| مليون ونص / milyon w nos | 1,500,000 |
| ربع مليون / rub3 milyon | 250,000 |
| مليون وربع | 1,250,000 |
| مليون إلا ربع / milyon ila rub3 | 750,000 |
| نص مليون | 500,000 |
| مليونين / مليونين ونص | 2,000,000 / 2,500,000 |
| ثلاث ملايين / أربع ملايين | 3,000,000 / 4,000,000 |
| مليون ومية ألف | 1,100,000 |
| مليون وخمسميّة | 1,500,000 |
| تلتمية / ثمنمية / ستمية / خمسمية / أربعمية | 300,000 / 800,000 / 600,000 / 500,000 / 400,000 (when followed by "ألف") |
| ميتين وخمسين ألف | 250,000 |
| سنة / سنة ونص / سنتين | 12 / 18 / 24 months |
| سنة وثمان شهور | 20 months |
| ستة شهور / ثمان شهور / خمس شهور / أربع شهور / ثلاث شهور | 6 / 8 / 5 / 4 / 3 months |
| sana / sana w nos / sanateen / sitta shhor | 12 / 18 / 24 / 6 months |

Rules for the expected values: a self-correction ("مليونين... لا لحظة، مليونين وربع") means the **last** figure; "a few millions", "a decent amount" or no figure at all means **null** and the expected action is `ask_again`; two incompatible incomes in the same chat mean the income is **null** (X3: re-ask, never store).
