Name       := example
Executable := $(Name).exe
ReportMD   := README.md
ReportTex  := $(Name).tex
ReportPDF  := $(Name).pdf
ReportCSV  := report.csv

ImplementationFolder := src
InterfaceFolder      := include

Sources != find $(ImplementationFolder) -name '*.c'
Objects := $(Sources:%.c=%.o)

CPPFLAGS += -I $(InterfaceFolder)
CFLAGS   += -g

build: $(Executable)
pdf: $(ReportPDF)
markdown: $(ReportMD)

clean:
	$(RM) $(Objects) $(ReportTex)

remove: clean
	$(RM) $(ReportMD) $(ReportPDF) $(Executable)

$(Executable): $(Objects)
	$(CC) $(CFLAGS) $(LDLFLAGS) $^ $(LDLIBS) -o $@

$(ReportCSV):
	PYTHONPATH='..' python -m qualamity -c ../.qualamity.yaml . -I include -f csv > $@

$(ReportMD):
	PYTHONPATH='..' python -m qualamity -c ../.qualamity.yaml . -I include > $@

$(ReportTex):
	PYTHONPATH='..' python -m qualamity -f latex -c ../.qualamity.yaml . -I include > $@

$(ReportPDF): $(ReportTex)
	tectonic $<
