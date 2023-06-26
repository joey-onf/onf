# -*- makefile -*-

# -*- makefile -*-

$(foreach jobdir,$(job-dir-opts),\
  $(foreach path,$(shell find $(jobdir) -mindepth 2 -maxdepth 2 -name 'config.xml'),\
    $(foreach subdir,$(patsubst %/,%,$(dir $(path))),\
        $(foreach name,$(notdir $(subdir)),\
           $(eval job-dir += $(name))\
        )\
    )\
  )\
)

$(foreach job,$(sort $(job-dir)),$(info job: $(job)))

# [EOF]
