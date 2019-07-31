
T_trimmed = len(UAV_times_trimmed)
height_extractor = np.zeros(( T_trimmed, nv*T_trimmed ))
    for i in range(T_trimmed):
        height_extractor[ i, nv*i ] = 1

b_vec = distance_hor < ds

# SAFETY CONSTRAINT
# dl - ds < 0 --> Automatically satisfied in b == 0
(dl - ds)*height_extractor*xv <= np.diag(b_vec)*(hs*dl - hs*distance_hor)
(dl - ds)*height_extractor*xv <= np.diag(b_vec)*(hs*dl + hs*distance_hor)

# SAFE HEIGHT CONSTRAINT
# UAV height usually > 0 --> Automatically satisfied if b == 1
height_extractor*xv >= hs*(np.ones(T_trimmed, 1) - b_vec)

# # Safety constraints
# constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
#     <= cp.diag(self.b)*(params.hs*params.dl - params.hs*self.dist)]
# constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
#     <= cp.diag(self.b)*(params.hs*params.dl + params.hs*self.dist)]
# # Safe height constraints
# constraintsVert += [self.height_extractor*self.xv \
#     >= params.hs*(np.ones(( T+1, 1 )) - self.b)]
