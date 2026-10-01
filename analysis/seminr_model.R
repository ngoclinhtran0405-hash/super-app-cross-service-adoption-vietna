# PLS-SEM model specification (R, package `seminr`) — replicates the SmartPLS 4 model.
# NOTE: template written from the reported model; run it on the anonymised data in data/
# and compare with results/*.csv. Minor numeric differences vs SmartPLS are normal.
# install.packages("seminr")
library(seminr)

data <- read.csv("data/survey_anonymised.csv")

measurement <- constructs(
  composite("PPF", c("PPF1","PPF2","PPF3","PPF4")),
  composite("PBE", c("PBE2","PBE3","PBE4","PBE5","PBE7","PBE8","PBE9")),
  composite("PSP", c("PSP1","PSP2","PSP3","PSP4","PSP5","PSP6")),
  composite("SEQ", c("SEQ2","SEQ3","SEQ4","SEQ5","SEQ6")),
  composite("FSS", c("FSS1","FSS2","FSS3")),
  composite("SSS", c("SSS1","SSS2","SSS4")),
  composite("VSS", c("VSS1","VSS2","VSS3")),
  composite("HSS", c("HSS1","HSS2","HSS3","HSS4")),
  composite("CSA", c("CSA1","CSA2","CSA3")),
  composite("CL",  c("CL1","CL2","CL3","CL4","CL5","CL6","CL7")),
  composite("USE", c("USE1","USE2","USE3"))
)

mediators <- c("CL","CSA","FSS","HSS","SSS","VSS")
structural <- relationships(
  paths(from = c("PPF","PBE","PSP","SEQ"), to = mediators),
  paths(from = mediators, to = "USE")
)

model <- estimate_pls(data = data, measurement_model = measurement, structural_model = structural)
summary(model)                                   # loadings, reliability, HTMT, VIF, R2, f2

boot <- bootstrap_model(model, nboot = 5000, seed = 2025)
summary(boot)                                    # path coefficients, t-values, p-values

# Optional extension: indirect effects, e.g. SEQ -> CSA -> USE
specific_effect_significance(boot, from = "SEQ", through = "CSA", to = "USE")
