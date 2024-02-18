import argparse
import sys

from samples.list_samples import list_samples

print("IINIT")
print(sys.path)
print(__name__)

def main():
    arg_parser = argparse.ArgumentParser(
        prog="samples",
        description="Analize annotated samples"
    )
    
#     list_samples()


if __name__ == "__main__":
    list_samples("C:\\development\\temp\\merger_acquisition\\plx_core\\spacy_projects\\ma_spancat\\samples_from_prodigy.json")
