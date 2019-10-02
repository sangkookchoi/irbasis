import unittest
import numpy
import irbasis as ir
import math


class TestMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):

        super(TestMethods, self).__init__(*args, **kwargs)

    def test_small_lambda_f(self):
        for _lambda in [10.0, 1E+4, 1E+7]:
            prefix = "basis_f-mp-Lambda" + str(_lambda)
            rb = ir.basis("../irbasis.h5", prefix)
            check_data_ulx = rb._check_ulx()
            for _data in check_data_ulx:
                self.assertLessEqual(_data[2], 1e-11)

            check_data_vly = rb._check_vly()
            for _data in check_data_vly:
                self.assertLessEqual(_data[2], 1e-11)

    def test_small_lambda_b(self):
        for _lambda in [10.0, 1E+4, 1E+7]:
            prefix = "basis_b-mp-Lambda" + str(_lambda)
            rb = ir.basis("../irbasis.h5", prefix)
            check_data_ulx = rb._check_ulx()
            for _data in check_data_ulx:
                self.assertLessEqual(_data[2], 1e-11)

            check_data_vly = rb._check_vly()
            for _data in check_data_vly:
                self.assertLessEqual(_data[2], 1e-11)

    def test_differential_ulx(self):
        for _lambda in [10.0, 1E+4, 1E+7]:
            prefix = "basis_f-mp-Lambda" + str(_lambda)
            rb_np8 = ir.basis("../irbasis.h5", prefix)
            d_ulx_ref_np8 = rb_np8._get_d_ulx_ref()
            d_ulx_ref_np8_1st = d_ulx_ref_np8[d_ulx_ref_np8[:, 2] == 1][0][3]
            d_ulx_ref_np8_2nd = d_ulx_ref_np8[d_ulx_ref_np8[:, 2] == 2][0][3]
            # 1-st differential
            Nl = rb_np8.dim()
            if Nl % 2 == 1: Nl -= 1
            d_1st_differential = abs((d_ulx_ref_np8_1st - rb_np8.d_ulx(Nl-1, 1.0, 1)) / d_ulx_ref_np8_1st)
            self.assertLessEqual(d_1st_differential, 1e-11)
            # 2-nd differential
            d_2nd_differential = abs((d_ulx_ref_np8_2nd - rb_np8.d_ulx(Nl-1, 1.0, 2)) / d_ulx_ref_np8_2nd)
            self.assertLessEqual(d_2nd_differential, 1e-11)

    def test_vectorization(self):
        for _lambda in [1E+4]:
            prefix = "basis_f-mp-Lambda" + str(_lambda)
            rb = ir.basis("../irbasis.h5", prefix)

            # re-vectorized functions
            revec_ulx = numpy.vectorize(rb.ulx)
            revec_vly = numpy.vectorize(rb.vly)
            revec_sl = numpy.vectorize(rb.sl)

            # check that those match:
            x = numpy.array([-.3, .2, .5])
            l = numpy.array([1, 3, 10, 15], dtype=int)
            alll = numpy.arange(rb.dim())

            self.assertTrue(numpy.allclose(revec_sl(l), rb.sl(l)))
            self.assertTrue(numpy.allclose(revec_sl(alll), rb.sl()))

            self.assertTrue(numpy.allclose(revec_ulx(l[0], x), rb.ulx(l[0], x)))
            self.assertTrue(numpy.allclose(revec_ulx(l, x[0]), rb.ulx(l, x[0])))
            self.assertTrue(numpy.allclose(revec_ulx(alll, x[0]),
                                           rb.ulx(None, x[0])))
            self.assertTrue(numpy.allclose(revec_ulx(l[:,None], x[None,:]),
                                           rb.ulx(l[:,None], x[None,:])))

            self.assertTrue(numpy.allclose(revec_vly(l[0], x), rb.vly(l[0], x)))
            self.assertTrue(numpy.allclose(revec_vly(l, x[0]), rb.vly(l, x[0])))
            self.assertTrue(numpy.allclose(revec_vly(alll, x[0]),
                                           rb.vly(None, x[0])))
            self.assertTrue(numpy.allclose(revec_vly(l[:,None], x[None,:]),
                                           rb.vly(l[:,None], x[None,:])))



if __name__ == '__main__':
    unittest.main()

# https://cmake.org/pipermail/cmake/2012-May/050120.html
