{ stdenv
, mkRosPackage
, robonomics_comm-nightly
, python3Packages
}:

mkRosPackage rec {
  name = "${pname}-${version}";
  pname = "roomba980_worker";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = with python3Packages; [
    robonomics_comm-nightly
    pyyaml
    ipfshttpclient
  ];

  meta = with stdenv.lib; {
    description = "Agent that offers data from sensors";
    homepage = http://github.com/airalab/sensors-connectivity;
    license = licenses.bsd3;
    maintainers = with maintainers; [ vourhey ];
  };
}
