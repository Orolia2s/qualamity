Name       := example
Executable := $(Name).exe
ReportMD   := README.md
ReportTex  := $(Name).tex
ReportPDF  := $(Name).pdf
ReportCSV  := $(Name).csv

ImplementationFolder := src
InterfaceFolder      := include

Qualamity := uv run qualamity
Run       := $(Qualamity) -c ../.qualamity.yaml -I include src include

Sources != find $(ImplementationFolder) -name '*.c'
Objects := $(Sources:%.c=%.o)

CPPFLAGS += -I $(InterfaceFolder)
CFLAGS   += -g

build: $(Executable)
pdf: $(ReportPDF)
markdown: $(ReportMD)
csv: $(ReportCSV)

clean:
	$(RM) $(Objects) $(ReportTex)

remove: clean
	$(RM) $(ReportMD) $(ReportPDF) $(Executable) $(ReportCSV)

$(Executable): $(Objects)
	$(CC) $(CFLAGS) $(LDLFLAGS) $^ $(LDLIBS) -o $@

$(ReportCSV):
	$(Run) -f csv > $@

$(ReportMD):
	$(Run) -f markdown > $@

$(ReportTex):
	$(Run) -f latex > $@

$(ReportPDF): $(ReportTex)
	tectonic $<
