rule all:
    input:
        'latex/build/CP-in-B-example.pdf',

rule preprocess_data:
    input:
        script = 'scripts/preprocess_data.py',
        magdown_fn = 'input/data/B2HHH_MagnetDown.root',
        magup_fn = 'input/data/B2HHH_MagnetUp.root',
    output:
        fn = 'output/data/B2{products}.root',
    shell:
        '{input.script} --input-fn {input.magdown_fn} {input.magup_fn}'
        ' --output-fn {output.fn} --products {wildcards.products}'

rule plot_histograms:
    input:
        script = 'scripts/plot_mass.py',
        fn = 'output/data/{channel}.root',
        config = 'config/mass_window.json',
    output:
        mass_fn = 'output/plots/{channel}/B_M.pdf',
        p_fn = 'output/plots/{channel}/B_P.pdf',
    shell:
        '{input.script} --input-fn {input.fn} --mass-fn {output.mass_fn}'
        ' --p-fn {output.p_fn} --key {wildcards.channel}'


rule plot_2d:
    input:
        script = 'scripts/plot_dalitz.py',
        fn = 'output/data/{channel}.root',
        config = 'config/mass_window.json',
    output:
        bplus_dalitz_fn = 'output/plots/{channel}/Bp_dalitz.pdf',
        bminus_dalitz_fn = 'output/plots/{channel}/Bm_dalitz.pdf',
        cp_plot_fn = 'output/plots/{channel}/CP.pdf',
        integrated_tex_fn = 'output/latex/{channel}/integrated.tex',
    shell:
        '{input.script} --input-fn {input.fn} --key {wildcards.channel}'
        ' --bplus-dalitz-fn {output.bplus_dalitz_fn} --bminus-dalitz-fn {output.bminus_dalitz_fn}'
        ' --cp-plot-fn {output.cp_plot_fn} --integrated-tex-fn {output.integrated_tex_fn}'


rule make_pdf:
    input:
        'latex/CP-in-B-example.tex',
        ['output/plots/B2KKK/B_M.pdf', 'output/plots/B2KKK/Bp_dalitz.pdf', 'output/plots/B2KKK/Bm_dalitz.pdf'],
        ['output/plots/B2KKPi/B_M.pdf', 'output/plots/B2KKPi/Bp_dalitz.pdf', 'output/plots/B2KKPi/Bm_dalitz.pdf'],
        ['output/plots/B2KPiPi/B_M.pdf', 'output/plots/B2KPiPi/Bp_dalitz.pdf', 'output/plots/B2KPiPi/Bm_dalitz.pdf'],
        ['output/plots/B2PiPiPi/B_M.pdf', 'output/plots/B2PiPiPi/Bp_dalitz.pdf', 'output/plots/B2PiPiPi/Bm_dalitz.pdf'],
    output:
        'latex/build/CP-in-B-example.pdf',
    shell:
        'cd latex && make'
