import materialdatabase as mdb
import numpy as np

mdb_instance = mdb.MaterialDatabase()

initial_mu_r_abs = mdb_instance.get_material_attribute(material_name="N95", attribute="initial_permeability")


core_material_resistivity = mdb_instance.get_material_attribute(material_name="N95", attribute="resistivity")


b_ref, mu_r_real, mu_r_imag = mdb_instance.permeability_data_to_pro_file(temperature=25, frequency=150000,
                                                                         material_name="N95",
                                                                         datatype=mdb.MeasurementDataType.ComplexPermeability,
                                                                         datasource=mdb.MaterialDataSource.ManufacturerDatasheet,
                                                                         parent_directory="")

b_ref = np.array(b_ref)

b_test_ref = np.array([0.0, 0.14285714, 0.28571429, 0.42857143, 0.57142857, 0.71428571, 0.85714286, 1.0])
mu_r_real_test_ref = np.array([1., 438.42857143, 550.71428571, 560., 560., 560., 560., 560.])
mu_r_imag_test_ref = np.array([3.00000000e+03, 2.96707143e+03, 2.95635714e+03, 1.00000000e+00,
                               1.00000000e+00, 1.00000000e+00, 1.00000000e+00, 1.00000000e+00])

epsilon_r, epsilon_phi_deg = mdb_instance.get_permittivity(temperature=25, frequency=150000, material_name="N95",
                                                           datasource=mdb.MaterialDataSource.Measurement,
                                                           datatype=mdb.MeasurementDataType.ComplexPermittivity,
                                                           measurement_setup="LEA_LK", interpolation_type="linear")