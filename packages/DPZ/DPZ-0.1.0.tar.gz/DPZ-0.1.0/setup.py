import setuptools

# Encuentra los paquetes del proyecto
found_packages = setuptools.find_packages(where="src")

# Imprime los nombres de los paquetes encontrados
print("Paquetes encontrados:", found_packages)


with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DPZ",
    version="0.1.0",
    author="Antonio Vila",
    author_email="vila.antoniojose@gmail.com",
    description="Obtén el precio del dólar en Venezuela desde múltiples fuentes con una sola línea de código! Con funciones de webscraping integradas, recopilamos y consolidamos los datos más actualizados",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntonioVilaV/dolar-price-vzla",
    package_dir={"": "src"},
    packages=found_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
