
# C2DLL

### Easily build C code into dll and call it from python script

Here is the example of usage:

```python
from c2dll import dllfunc, as_ptr
import numpy as np

def fwd(eps, n, x=[0.1711, 0.1117]):
    d = dllfunc('''
        #define PI2 6.283185307179586
        #include <math.h>

        double mod1(double x) {double x_mod_1 = fmod(x, 1); x_mod_1 = (x_mod_1 < 0) ? x_mod_1 + 1 : x_mod_1; return x_mod_1;}
                
        DLL_API void fwd(double* params, double* x, int n, double* out) {
            double eps_square = params[0]*params[0]; 
            for (int i=0; i<n; i++) { 
                double x_ = atan2((1 - eps_square) * sin(PI2 * x[0]), (1 + eps_square) * cos(PI2 * x[0]) + 2*params[0]) / PI2;
                x[0] = 2 * x_ + x[1];
                x[1] = x_ + x[1];
                x[0] = atan2((1 - eps_square) * sin(PI2 * x[0]), (1 + eps_square) * cos(PI2 * x[0]) + 2*params[0]) / PI2;
                x[0] = mod1(x[0]);
                x[1] = mod1(x[1]);
                out[2*i] = x[0];
                out[2*i+1] = x[1];
            }
        }''')
    n = int(n)
    points = np.zeros(shape=(2*n))
    d.fwd(as_ptr([eps,]), as_ptr(x), n, as_ptr(points))
    return points.reshape((n, 2))
```


GitHub: https://github.com/chiga17/c2dll
