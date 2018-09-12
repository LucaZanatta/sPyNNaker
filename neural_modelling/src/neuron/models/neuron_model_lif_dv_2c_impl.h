#ifndef _NEURON_MODEL_LIF_CURR_DV_2C_IMPL_H_
#define _NEURON_MODEL_LIF_CURR_DV_2C_IMPL_H_

#include "neuron_model.h"

/////////////////////////////////////////////////////////////
// definition for LIF neuron parameters
typedef struct neuron_t {
    // membrane voltage [mV]
    REAL     V_membrane;

    // membrane resting voltage [mV]
    REAL     V_rest;

    // membrane resistance [MOhm]
    REAL     R_membrane;

    // 'fixed' computation parameter - time constant multiplier for
    // closed-form solution
    // exp(-(machine time step in ms)/(R * C)) [.]
    REAL     exp_TC;

    // offset current [nA]
    REAL     I_offset;

    // countdown to end of next refractory period [timesteps]
    int32_t  refract_timer;

    // post-spike reset membrane voltage [mV]
    REAL     V_reset;

    // refractory time of neuron [timesteps]
    int32_t  T_refract;

    // prev step voltage
    REAL     V_prev;

    //low-pass filtered version of voltage (Ca???)
    REAL     V_slow;

    // filtered-voltage change in time
    REAL     dV_dt_slow;

    // low-pass weight
    REAL     gamma;
    REAL     gamma_complement;

    REAL     V_max;
    REAL     V_spike;
    
    REAL     V2_membrane;

} neuron_t;

typedef struct global_neuron_params_t {
} global_neuron_params_t;

#endif // _NEURON_MODEL_LIF_CURR_DV_IMPL_H_
