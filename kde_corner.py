import arviz
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from copy import copy, deepcopy


def kde_corner(arviz_data,
               var_names,
               arviz_kwargs = None,
               marginals=True,
               points_estimate="mean",
               kind="kde",
               colormap=cm.inferno,
               figsize=(12,12),
               save=None
              ):

    arfit = copy(arviz_data)

    arviz_kwargs_default = {'kde_kwargs' : { 'hdi_probs': [0.25, 0.5, 0.75, 0.95],
                                             'contourf_kwargs': { 'cmap': colormap,  
                                                                },
                                             'contour_kwargs': { 'levels': 6,  
                                                                 'colors': ['none'] * 6 ,  
                                                                 'zorder': 9
                                                               },
                                             'fill_last': False  
                                             },
                            
                            'marginal_kwargs' : {'plot_kwargs': {'color': 'black'}
                                                },
                            
                            'scatter_kwargs': {'s': 1, 'alpha': 1, 'zorder': -1
                                              },
                            'hexbin_kwargs': {'mincnt' : len(arfit.posterior[var_names[0]].values.flatten()) / len(arfit.posterior[var_names[0]]) * 0.02,
                                              'cmap' : colormap
                                             }
                            }
                 
    
    updated_kwargs = deepcopy(arviz_kwargs_default)
    if arviz_kwargs is not None:
        for key, value in arviz_kwargs.items():
            if key in updated_kwargs and isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    updated_kwargs[key][nested_key] = nested_value
            else:
                updated_kwargs[key] = value
    else:
        pass

    updated_kwargs['kde_kwargs'].update({'contourf_kwargs': { 'cmap': colormap,  
                                                            }
                                        })
    
    updated_kwargs['hexbin_kwargs'].update({'hexbin_kwargs': { 'cmap': colormap,  
                                                            }
                                        })
    print(updated_kwargs)
    fig, axes = plt.subplots(nrows=len(var_names), ncols=len(var_names), figsize=figsize)
    
    arviz.plot_pair(
        arfit,
        var_names=var_names,
        marginals=marginals,
        point_estimate=points_estimate,
        kind=kind,
        ax=axes,
        **updated_kwargs,
        show=False
    )
    
    summary = arviz.summary(arfit)
    
    xlabels = [axes[-1,j].get_xlabel() for j in range(len(var_names))]
    ylabels = [axes[i, 0].get_ylabel() for i in range(len(var_names))]
    
    if len(var_names) == 2:
        axes[1, 0].scatter(
                arfit.posterior[xlabels[0]].values.flatten(),  
                arfit.posterior[ylabels[1]].values.flatten(),  
                s=updated_kwargs['scatter_kwargs']['s'],  # Marker size
                color=updated_kwargs['kde_kwargs']['contourf_kwargs']['cmap'](0),  
                alpha=updated_kwargs['scatter_kwargs']['alpha'],
                zorder=updated_kwargs['scatter_kwargs']['zorder']
            )

        pf = "+" + str(round(summary.loc[xlabels[0]]['hdi_97%'] - summary.loc[xlabels[0]][points_estimate],2))
        pn = str(round(summary.loc[xlabels[0]]['hdi_3%'] - summary.loc[xlabels[0]][points_estimate], 2))
        
        axes[0,0].set_title(f"{xlabels[0]}={summary.loc[xlabels[0]]['mean']:.2f}$_{{{pn}}}^{{{pf}}}$")


        pf = "+" + str(round(summary.loc[ylabels[1]]['hdi_97%'] - summary.loc[ylabels[1]][points_estimate],2))
        pn = str(round(summary.loc[ylabels[1]]['hdi_3%'] - summary.loc[ylabels[1]][points_estimate], 2))
        
        axes[1,1].set_title(f"{ylabels[1]}={summary.loc[ylabels[1]]['mean']:.2f}$_{{{pn}}}^{{{pf}}}$")
        
    else:
        for i in range(len(axes)):
            for j in range(len(axes)):
                if i != j:
                    axes[i, j].scatter(
                        arfit.posterior[xlabels[j]].values.flatten(),  
                        arfit.posterior[ylabels[i]].values.flatten(),  
                        s=updated_kwargs['scatter_kwargs']['s'], 
                        color=updated_kwargs['kde_kwargs']['contourf_kwargs']['cmap'](0),  
                        alpha=updated_kwargs['scatter_kwargs']['alpha'],
                        zorder=updated_kwargs['scatter_kwargs']['zorder']
                    )

        for j in range(len(axes)):
            pf = "+" + str(round(summary.loc[xlabels[j]]['hdi_97%'] - summary.loc[xlabels[j]][points_estimate],2))
            pn = str(round(summary.loc[xlabels[j]]['hdi_3%'] - summary.loc[xlabels[j]][points_estimate], 2))
            
            axes[j, j].set_title(f"{xlabels[j]}={summary.loc[xlabels[j]]['mean']:.2f}$_{{{pn}}}^{{{pf}}}$")
        
    plt.tight_layout()
    if save is not None:
        plt.savefig(save)
    plt.close()
    return fig
