import arviz
import numpy as np

def load_emcee(emcee_sampler, var_names, burn=0.1, thin=2):
  """arviz.from_emcee does not work properly. This function perpares a dictionary to load the emcee result
  using arviz.from_dict method.
  """
  nvarys = len(var_names)
  nstep = emcee_sampler.iteration
  chains = emcee_sampler.get_chain(discard=burn if burn>1 else burn * nstep, thin=thin)
  log_prob = emcee_sampler.get_log_prob(discard=burn if burn>1 else burn * nstep, thin=thin)
  idata = az.from_dict(
    posterior={
        var: chains[:, :, i] for i, var in enumerate(var_names)
    },
    log_likelihood={"obs": log_prob}
  )
  return idata
