#include "timing_pair_supervision_impl.h"

//---------------------------------------
// Globals
//---------------------------------------
// Exponential lookup-tables
int16_t tau_plus_lookup[TAU_PLUS_SIZE];
int16_t tau_minus_lookup[TAU_MINUS_SIZE];
int16_t tau_c_lookup[TAU_C_SIZE];
int16_t tau_d_lookup[TAU_D_SIZE];
int32_t weight_update_constant_component=0;

//---------------------------------------
// Functions
//---------------------------------------
address_t timing_initialise(address_t address) {

    log_info("timing_initialise: starting");
    log_info("\tSTDP - NeuroModulated pair rule");
    // **TODO** assert number of neurons is less than max

    // Copy LUTs from following memory
    address_t lut_address = maths_copy_int16_lut(&address[0], TAU_PLUS_SIZE,
                                                 &tau_plus_lookup[0]);
    lut_address = maths_copy_int16_lut(lut_address, TAU_MINUS_SIZE,
                                       &tau_minus_lookup[0]);
    lut_address = maths_copy_int16_lut(lut_address, TAU_C_SIZE,
                                       &tau_c_lookup[0]);
    lut_address = maths_copy_int16_lut(lut_address, TAU_D_SIZE,
                                       &tau_d_lookup[0]);

    // Read Izhikevich weight update equation constant component
    weight_update_constant_component = *lut_address++;

    log_info("weight_update_constant_component = %d", 
             weight_update_constant_component);
    
    log_info("timing_initialise: completed successfully");

    return lut_address;
}