Executable := example.exe

ImplementationFolder := src
InterfaceFolder      := include

Sources != find $(ImplementationFolder) -name '*.c'
Objects := $(Sources:%.c=%.o)

CPPFLAGS += -I $(InterfaceFolder)
CFLAGS   += -g

$(Executable): $(Objects)
	$(CC) $(CFLAGS) $(LDLFLAGS) $^ $(LDLIBS) -o $@

report:
	PYTHONPATH='..' python -m qualamity -c ../.qualamity.yaml . -I include > README.md

clean:
	$(RM) $(Objects)
