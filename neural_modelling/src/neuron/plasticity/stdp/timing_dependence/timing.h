#ifndef _TIMING_H_
#define _TIMING_H_

#include "../synapse_structure/synapse_structure.h"

typedef int16_t stp_trace_t;
address_t timing_initialise(address_t address);

static post_trace_t timing_get_initial_post_trace();

static post_trace_t timing_add_post_spike(uint32_t time, uint32_t last_time,
                                          post_trace_t last_trace);

static pre_trace_t timing_add_pre_spike(uint32_t time, uint32_t last_time,
                                        pre_trace_t last_trace);

static update_state_t timing_apply_pre_spike(
    uint32_t time, pre_trace_t trace, uint32_t last_pre_time,
    pre_trace_t last_pre_trace,  uint32_t last_post_time,
    post_trace_t last_post_trace, update_state_t previous_state);

static update_state_t timing_apply_post_spike(
    uint32_t time, post_trace_t trace, uint32_t last_pre_time,
    pre_trace_t last_pre_trace, uint32_t last_post_time,
    post_trace_t last_post_trace, update_state_t previous_state);

static inline stp_trace_t timing_decay_stp_trace(
        uint32_t time, uint32_t last_time, stp_trace_t last_stp_trace,
		uint16_t P_Baseline, uint16_t stp_type);

static inline stp_trace_t timing_apply_stp_spike(
        uint32_t time, uint32_t last_time, stp_trace_t last_stp_trace,
		uint16_t P_Baseline, uint16_t stp_type);

#endif // _TIMING_H_
