import math
import os

def wsp_nail_slip_en(nail, vn, moisture_content, structural1=True):
    # SDPWS 2021 Table C4.2.3D
    if nail == "6d":
        if moisture_content > 19:
            en = math.pow(vn / 434, 2.314)
        else:
            en = math.pow(vn / 456, 3.144)
    elif nail == "8d":
        if moisture_content > 19:
            en = math.pow(vn / 857, 1.869)
        else:
            en = math.pow(vn / 616, 3.018)
    elif nail == "10d":
        if moisture_content > 19:
            en = math.pow(vn / 977, 1.894)
        else:
            en = math.pow(vn / 769, 3.276)
    else:
        en = 10

    if not structural1:
        # SDPWS 2021 Table C4.2.3D - Footnote 1
        # The slip shall be increased by 20 percent when plywood or OSB is not Structural I.
        en = 1.20 * en

    return en


def four_term_deflection(
    V_plf, H_ft, E_psi, A_sqin, b_ft, Gt_lbpin, en_in, holddown_data, additional_end_chord_force_lbs=0
):

    # Term 1 Bending Deflection - 8 v h^3 / E A b
    delta_bending_in = (8 * V_plf * H_ft * H_ft * H_ft) / (E_psi * A_sqin * b_ft)

    # Term 2 - Shear Deflection - v h / Gt
    delta_shear_in = (V_plf * H_ft) / Gt_lbpin

    # Term 3 - Fastener Slip - 0.75 h en
    delta_fastener_in = 0.75 * H_ft * en_in

    # Term 4 - Hold-Down Deformation - da h/b
    da = (holddown_data[1] * ((V_plf * H_ft)+additional_end_chord_force_lbs))/ holddown_data[0]
    delta_holddown_in = da * (H_ft / b_ft)

    delta_in = delta_bending_in + delta_shear_in + delta_fastener_in + delta_holddown_in

    return {
        "delta": delta_in,
        "delta_bending": delta_bending_in,
        "delta_shear": delta_shear_in,
        "delta_fastener": delta_fastener_in,
        "delta_holddown": delta_holddown_in,
    }


if __name__ == "__main__":
    # FTAO Panel Anaysis following APA T555
    errors = []
    warnings = []
    tick_count = 100

    #### BEGIN INPUTS ####
    ######################

    '''
    ## APA T555 Inputs ##

    V_lbs = 3750  # Shear for force analysis
    Vdelta_lbs = 5357  # Shear for Deformation Analysis
    Hwall_ft = 8  # Total height of Wall Panel
    endchord_above_lbs = 0  # Chord Force from Wall Panel Above Current Panel

    hb_ft = 4  # Sill Height of Openings
    ho_ft = 2.67  # Height of Openings

    piers = [4,4,3.5]  # List of Pier Widths
    openings = [6,2]  # List of Opening Widths

    Cd = 4.0
    E_psi = 1600000  # Elastic Modulus of the end posts
    A_sqin = 16.5  # Area of the end posts
    Gt_lbpin = 83500  # Shear Stiffness through the depth of the sheathing
    nail = "8d"  # nail size as a string 6d, 8d, or 10d no others supported.
    nail_spacing_in = 4  # nail spacing
    moisture_content = 19  # moisture content of lumber used for nail slip calc, typically 19 or less
    hdcapacity_lbs = 2145  # Hold Down Capacity as provided by the manufacturer
    hddelta_in = 0.128  # Hold Down Deformation at capacity as provided by the manufacturer
    holddown_data = [hdcapacity_lbs, hddelta_in]  # Hold Down Data as List for input into deformation function
    Structural1 = False
    
    ## END APA T555 Inputs ##
    '''
    # Inputs For Analysis
    V_lbs = 4117.2  # Shear for force analysis
    Vdelta_lbs = 4117.2  # Shear for Deformation Analysis
    Hwall_ft = 10.67  # Total height of Wall Panel
    endchord_above_lbs = 1155  # Chord Force from Wall Panel Above Current Panel

    hb_ft = 1.33  # Sill Height of Openings
    ho_ft = 6.32  # Height of Openings

    piers = [5,7.33,5.02]  # List of Pier Widths
    openings = [7.33,7.33]  # List of Opening Widths

    # Inputs for Deflection
    Cd = 1.0
    E_psi = 1400000  # Elastic Modulus of the end posts
    A_sqin = 16.5  # Area of the end posts
    Gt_lbpin = 83500  # Shear Stiffness through the depth of the sheathing
    nail = "8d"  # nail size as a string 6d, 8d, or 10d no others supported.
    nail_spacing_in = 6  # nail spacing
    moisture_content = 19  # moisture content of lumber used for nail slip calc, typically 19 or less
    hdcapacity_lbs = 3285  # Hold Down Capacity as provided by the manufacturer
    hddelta_in = 0.114  # Hold Down Deformation at capacity as provided by the manufacturer
    holddown_data = [hdcapacity_lbs, hddelta_in]  # Hold Down Data as List for input into deformation function
    Structural1 = True

    #### END INPUTS ####
    ######################

    if len(piers) != len(openings) + 1:
        errors.append(
            f"Pier count not consistent with openings, # piers should be {len(openings)+1} but is {len(piers)}"
        )

    if hb_ft <= 0 :
        errors.append(f"Sill height, hb, of {hb_ft} ft must be greater than 0")
    if hb_ft+ho_ft >= Hwall_ft-0.5:
        errors.append(f"Opening too large")

    # Basic computed values
    ha_ft = Hwall_ft - hb_ft - ho_ft  # height above opening
    Lwall_ft = sum(piers) + sum(openings)  # total wall length
    basic_unit_shear_plf = V_lbs / Lwall_ft  # basic unit shear V/L

    print("-" * tick_count)
    print("Inputs and Geometry:")
    print(f"Applied Shear, V: {V_lbs:.3f} lbs")
    print(f"Applied Shear For Deflection, Vdelta: {Vdelta_lbs:.3f} lbs")
    print(f"Chord Force from Above, Habove = {endchord_above_lbs:.3f} lbs")
    print(f"Wall Panel Height, Hw: {Hwall_ft:.3f} ft")
    print(f"Opening Sill Height, Hb: {hb_ft:.3f} ft")
    print(f"Opening Height, Ho: {ho_ft:.3f} ft")
    print(f"Height above Opening, Ha: {ha_ft:.3f} ft")
    print("Piers:")
    for i, j in enumerate(piers):
        print(f"Lp{i+1} length: {j:.3f} ft")

    print("Openings:")
    for i, j in enumerate(openings):
        print(f"Lo{i+1} width: {j:.3f} ft")
    print(f"Total Wall Panel Length, L: {Lwall_ft:.3f} ft")

    # Compute aspect ratios
    # min pier of 2 ft required
    pier_ar = [ho_ft / i for i in piers]

    for i, j in enumerate(pier_ar):
        if piers[i] < 2.0:
            errors.append(f"Pier {i+1} length < 2.0 ft")
        if j > 3.5:
            errors.append(f"pier {i+1} aspect ratio of {j} exceeds 3.5:1 maximum.")

    print("-" * tick_count)
    print("Pier Aspect Ratios Ho/Lpi:")
    for i, j in enumerate(pier_ar):
        print(f"P{i+1} aspect ratio = {j:.3f}")

    # Compute pier adjustment factors
    # Method 1 = 2 bs/h
    method1_af = [
        2 * j * (1 / ho_ft) if pier_ar[i] > 2 else 1 for i, j in enumerate(piers)
    ]
    # Method 2 = 1.25 - (0.125 h/bs)
    method2_af = [
        1.25 - (0.125 * (ho_ft / j)) if pier_ar[i] > 2 else 1
        for i, j in enumerate(piers)
    ]

    print("-" * tick_count)
    print("Pier Adjustment Factors - Method 1 2*Lpi/ho:")
    for i, j in enumerate(method1_af):
        print(f"P{i+1} method 1 adjustment = {j:.3f}")

    print("Pier Adjustment Factors - Method 2 1.25 - (0.125*ho/Lpi):")
    for i, j in enumerate(method2_af):
        print(f"P{i+1} method 2 adjustment = {j:.3f}")

    # If no errors continue into the analysis otherwise print the errors
    if not errors:
        # Compute the Hold Down Force V*H/L
        hd_force_lbs = ((V_lbs * Hwall_ft) + (endchord_above_lbs * Lwall_ft)) * (
            1 / Lwall_ft
        )
        print("-" * tick_count)
        print(f"Hold Down Force, H: {hd_force_lbs:.3f} lbs")
        # Compute vertical unit shears @ section cuts of each window
        # assumes unit shear is equivalent in the top and bottom section
        # and via statics Sum of Unit shears = hold down force - end chord above force
        opening_shears_plf = [
            (hd_force_lbs - endchord_above_lbs) / (ha_ft + hb_ft) for i in openings
        ]

        print("-" * tick_count)
        print("Opening Unit Shears:")
        for i, j in enumerate(opening_shears_plf):
            print(f"va{i+1} = vb{i+1} = (H - Habove) / Ha+Hb = {j:.3f} plf")

        # Compute opening boundary forces = opening unit shear * opening width
        opening_boundary_force_lbs = [
            opening_shears_plf[i] * j for i, j in enumerate(openings)
        ]

        print("-" * tick_count)
        print("Opening Boundary Forces above and below opening:")
        for i, j in enumerate(opening_boundary_force_lbs):
            print(f"O{i+1} = va{i+1}*Lo{i+1} = {j:.3f} lbs")

        # Compute opening corner forces and Tributary Lengths
        corner_forces_lbs = []
        opening_tributaries_ft = []
        for i, j in enumerate(openings):
            left = piers[i]
            right = piers[i + 1]

            fleft = opening_boundary_force_lbs[i] * left * (1 / (left + right))
            fright = opening_boundary_force_lbs[i] * right * (1 / (left + right))

            corner_forces_lbs.append([fleft, fright])

            Tleft = j * left * (1 / (left + right))
            Tright = j * right * (1 / (left + right))

            opening_tributaries_ft.append([Tleft, Tright])

        print("-" * tick_count)
        print("Corner Forces:")
        for i, j in enumerate(corner_forces_lbs):
            print(f"FO{i+1},left = O{i+1}*L{i+1} / (L{i+1}+L{i+2}) = {j[0]:.3f} lbs")
            print(f"FO{i+1},right = O{i+1}*L{i+2} / (L{i+1}+L{i+2}) = {j[1]:.3f} lbs")

        print("-" * tick_count)
        print("Opening Tributaries:")
        for i, j in enumerate(opening_tributaries_ft):
            print(f"T{i+1},left = Lo{i+1}*L{i+1} / (L{i+1}+L{i+2}) = {j[0]:.3f} ft")
            print(f"T{i+1},right = Lo{i+1}*L{i+2} / (L{i+1}+L{i+2}) = {j[1]:.3f} ft")

        # Compute pier unit shears adjacent to the openings
        pier_shears_plf = []
        for i, j in enumerate(piers):

            # (V/L * (pier length + sum of tributaries))/pier length
            effective_length_ft = j
            if i == 0:
                # first pier only one tributary from left of first opening
                effective_length_ft += opening_tributaries_ft[i][0]
            elif i == len(piers) - 1:
                # last pier only one tributary from right of last opening
                effective_length_ft += opening_tributaries_ft[i - 1][1]
            else:
                # inteiror pier tributaries from right of left opening and left of right opening
                effective_length_ft += opening_tributaries_ft[i][0]
                effective_length_ft += opening_tributaries_ft[i - 1][1]

            unit_shear_plf = (basic_unit_shear_plf * effective_length_ft) / j

            pier_shears_plf.append(unit_shear_plf)

        print("-" * tick_count)
        print("Unit Shear in Pier adjacent to Opening:")
        for i, j in enumerate(pier_shears_plf):
            print(f"v{i+1} = {j:.3f} plf")

        # Check unit shears equal the applied load
        check_pier_shear_lbs = sum(
            [j * pier_shears_plf[i] for i, j in enumerate(piers)]
        )
        print(f"check that pier shears match applied load:")
        print(f"Sum of Pier Shears = {check_pier_shear_lbs:.3f} lbs")
        print(f"V = {V_lbs:.3f} lbs")
        print(f"Validated: {math.isclose(check_pier_shear_lbs,V_lbs)}")

        if not math.isclose(check_pier_shear_lbs, V_lbs):
            errors.append(
                f"Sum of Pier Shears, {check_pier_shear_lbs:.3f} lbs does not match applied load {V_lbs:.3f} lbs"
            )

        # Resistance to Corner Forces
        resisting_forces_lbs = [j * pier_shears_plf[i] for i, j in enumerate(piers)]

        print("-" * tick_count)
        print("Pier Force Resisting Corner Forces:")
        for i, j in enumerate(resisting_forces_lbs):
            print(f"R{i+1} = {j:.3f} lbs")

        # Delta of force at corners and Corner Zone Unit Shears
        corner_force_delta_lbs = []
        corner_unit_shears_plf = []

        for i, j in enumerate(piers):

            force_lbs = resisting_forces_lbs[i]

            if i == 0:
                # first pier only one force from left of first opening
                force_lbs -= corner_forces_lbs[i][0]
            elif i == len(piers) - 1:
                # last pier only one force from right of last opening
                force_lbs -= corner_forces_lbs[i - 1][1]
            else:
                # inteiror pier forces from right of left opening and left of right opening
                force_lbs -= corner_forces_lbs[i][0]
                force_lbs -= corner_forces_lbs[i - 1][1]

            corner_force_delta_lbs.append(force_lbs)
            corner_unit_shears_plf.append(force_lbs / j)

        print("-" * tick_count)
        print("Difference in Corner Force:")
        for i, j in enumerate(corner_force_delta_lbs):
            print(f"Fc{i+1} = {j:.3f} lbs")
        print("-" * tick_count)
        print("Pier Corner Unit Shears:")
        for i, j in enumerate(corner_unit_shears_plf):
            print(f"vc{i+1} = {j:.3f} plf")

        # Check Vertical Shear at each end of piers
        check_vertical_shears_lbs = []
        for i, j in enumerate(piers):
            fleft = 0
            fright = 0
            if i == 0:
                fleft += corner_unit_shears_plf[i] * (ha_ft + hb_ft)
                fleft += pier_shears_plf[i] * ho_ft
                fleft += endchord_above_lbs

                fright += opening_shears_plf[i] * (ha_ft + hb_ft)
                fright -= corner_unit_shears_plf[i] * (ha_ft + hb_ft)
                fright -= pier_shears_plf[i] * (ho_ft)

            elif i == len(piers) - 1:
                fright += corner_unit_shears_plf[i] * (ha_ft + hb_ft)
                fright += pier_shears_plf[i] * ho_ft
                fright += endchord_above_lbs

                fleft += opening_shears_plf[i - 1] * (ha_ft + hb_ft)
                fleft -= corner_unit_shears_plf[i] * (ha_ft + hb_ft)
                fleft -= pier_shears_plf[i] * (ho_ft)

            else:
                fleft += corner_unit_shears_plf[i] * (ha_ft + hb_ft)
                fleft += pier_shears_plf[i] * ho_ft
                fleft -= opening_shears_plf[i - 1] * (ha_ft + hb_ft)

                fright += opening_shears_plf[i] * (ha_ft + hb_ft)
                fright -= corner_unit_shears_plf[i] * (ha_ft + hb_ft)
                fright -= pier_shears_plf[i] * (ho_ft)

            check_vertical_shears_lbs.extend([fleft, fright])

        print("-" * tick_count)
        print("Check of Vertical Shear Lines")
        for i, j in enumerate(check_vertical_shears_lbs):
            if i != 0 and j != check_vertical_shears_lbs[-1]:
                print(f"Line {i} sums to {j:.3f} lbs = 0 lbs: {math.isclose(j+1, 1)}")
                if not math.isclose(j + 1, 1):
                    errors.append(
                        f"Check of Vertical Shear Line {i} Failes, Line {i} sums to {j:.3f} lbs but should be 0 lbs"
                    )
            else:
                print(
                    f"Line {i} sums to {j:.3f} lbs = hold down force of {hd_force_lbs:.3f} lbs: {math.isclose(j, hd_force_lbs)}"
                )

                if not math.isclose(j, hd_force_lbs):
                    errors.append(
                        f"Check of Vertical Shear Line {i} Failed, Line {i} sums to {j:.3f} lbs but should be hold down force of {hd_force_lbs:.3f} lbs"
                    )

        # Required shear capacity
        unadjusted_required_unit_shear_plf = max(
            max(opening_shears_plf),
            max([abs(i) for i in corner_unit_shears_plf]),
            max([i for i in pier_shears_plf]),
        )

        method1_required_unit_shear_plf = max(
            max(opening_shears_plf),
            max([abs(i) for i in corner_unit_shears_plf]),
            max([j / method1_af[i] for i, j in enumerate(pier_shears_plf)]),
        )

        method2_required_unit_shear_plf = max(
            max(opening_shears_plf),
            max([abs(i) for i in corner_unit_shears_plf]),
            max([j / method2_af[i] for i, j in enumerate(pier_shears_plf)]),
        )

        print("-" * tick_count)
        print(
            f"Required Sheathing Capacity with no adjustment: {unadjusted_required_unit_shear_plf:.3f} plf"
        )
        print(
            f"Required Sheathing Capacity for Method 1 Adjustment: {method1_required_unit_shear_plf:.3f} plf"
        )
        print(
            f"Required Sheathing Capacity for Method 2 Adjustment: {method2_required_unit_shear_plf:.3f} plf"
        )

        # Required Strap Force
        required_strap_force_lbs = max(
            max([i[0] for i in corner_forces_lbs]),
            max([i[1] for i in corner_forces_lbs]),
        )
        print(f"Required Strap Force: {required_strap_force_lbs:.3f} lbs")

        print(f"Required Hold Down Force: {hd_force_lbs:.3f} lbs")
        print(f"Required Wall Anchorage Unit Shear: {basic_unit_shear_plf:.3f} plf")

        # 4 Term Deflection
        print("-" * tick_count)
        print("4-Term Deflection Analysis: ")
        
        pier_deflections_four_term = []

        unit_shear_delta_plf = Vdelta_lbs / Lwall_ft

        # Effective Height of Piers away from end is the height
        # above the window sill. The bottom panel assumed to act rigidly
        # up to the end pier.
        heff_ft = Hwall_ft - hb_ft

        # Deflection to the Right
        for i, j in enumerate(piers):

            if i == 0:
                Leff = j + opening_tributaries_ft[i][0]
                hd_add = endchord_above_lbs
            elif i == len(piers) - 1:
                Leff = j + opening_tributaries_ft[i - 1][1]
                heff_ft += hb_ft  # For load from left last pier should be full height
                hd_add = 0
            else:
                Leff = (
                    j + opening_tributaries_ft[i][0] + opening_tributaries_ft[i - 1][1]
                )
                hd_add = 0

            Leff = Leff / j
            v_pier = unit_shear_delta_plf * Leff
            v_nail = (nail_spacing_in / 12) * v_pier
            en_in = wsp_nail_slip_en(nail, v_nail, moisture_content, Structural1)
            delta = four_term_deflection(
                v_pier, heff_ft, E_psi, A_sqin, j, Gt_lbpin, en_in, holddown_data, hd_add
            )

            pier_deflections_four_term.append(delta.get("delta"))

            print("-" * tick_count)
            print(f"Pier{i+1} Right Deflection Contribution:")
            print(f"v,pier{i+1} = {v_pier:.3f} plf")
            print(f"H,eff{i+1} = {heff_ft:.3f} ft")
            print(f"v,nail{i+1} = {v_nail:.3f} plf")
            print(f"en{i+1} = {en_in:.3f} in")
            print(f"delta - bending term = {delta.get('delta_bending'):.3f} in")
            print(f"delta - shear term = {delta.get('delta_shear'):.3f} in")
            print(f"delta - nail slip term = {delta.get('delta_fastener'):.3f} in")
            print(f"delta - hold down term = {delta.get('delta_holddown'):.3f} in")
            print(f"delta{i+1} = {delta.get('delta'):.3f} in")

        # Reset Heff
        # For deflection to the left first pier should be full height
        # In the following the loop the first pier will calcute first so
        # adjust Heff after the first cycle
        heff_ft = Hwall_ft

        # Deflection to the Left
        for i, j in enumerate(piers):

            if i == 0:
                Leff = j + opening_tributaries_ft[i][0]
                hd_add = 0
            elif i == len(piers) - 1:
                Leff = j + opening_tributaries_ft[i - 1][1]
                hd_add = endchord_above_lbs
            else:
                if i == 1:
                    heff_ft -= (
                        hb_ft  # reduce pier height after first pier but not again
                    )
                Leff = (
                    j + opening_tributaries_ft[i][0] + opening_tributaries_ft[i - 1][1]
                )
                hd_add = 0

            Leff = Leff / j
            v_pier = unit_shear_delta_plf * Leff
            v_nail = (nail_spacing_in / 12) * v_pier
            en_in = wsp_nail_slip_en(nail, v_nail, moisture_content, Structural1)
            delta = four_term_deflection(
                v_pier, heff_ft, E_psi, A_sqin, j, Gt_lbpin, en_in, holddown_data, hd_add
            )

            pier_deflections_four_term.append(delta.get("delta"))

            print("-" * tick_count)
            print(f"Pier{i+1} Left Deflection Contribution:")
            print(f"v,pier{i+1} = {v_pier:.3f} plf")
            print(f"H,eff{i+1} = {heff_ft:.3f} ft")
            print(f"v,nail{i+1} = {v_nail:.3f} plf")
            print(f"en{i+1} = {en_in:.3f} in")
            print(f"delta - bending term = {delta.get('delta_bending'):.3f} in")
            print(f"delta - shear term = {delta.get('delta_shear'):.3f} in")
            print(f"delta - nail slip term = {delta.get('delta_fastener'):.3f} in")
            print(f"delta - hold down term = {delta.get('delta_holddown'):.3f} in")
            print(f"delta{i+1} = {delta.get('delta'):.3f} in")

        percent_drift = (Cd*sum(pier_deflections_four_term)/len(pier_deflections_four_term))/(Hwall_ft*12)
        delta_h_over = 1/percent_drift
        print("-" * tick_count)
        print(
            f"Average of 4-Term Deflections = {sum(pier_deflections_four_term)/len(pier_deflections_four_term):.3f} in"
        )
        print(f"% Drift  = (Cd * Delta) / (Hwall * 12): {percent_drift:.4f} %")
        print(f"Drift Ratio = (Hwall * 12) / (Cd * Delta)  = H/{delta_h_over:.1f}")
        print("*" * tick_count)

        if not errors:
            print("***")
            print("***  ---- Summary Results ----")
            print(
                f"***  Required Sheathing Capacity with no adjustment: {unadjusted_required_unit_shear_plf:.3f} plf"
            )
            print(
                f"***  Required Sheathing Capacity for Method 1 [2*Lpi/ho] Adjustment: {method1_required_unit_shear_plf:.3f} plf"
            )
            print(
                f"***  Required Sheathing Capacity for Method 2 [1.25 - (0.125*ho/Lpi)] Adjustment: {method2_required_unit_shear_plf:.3f} plf"
            )
            print(f"***  Required Strap Force: {required_strap_force_lbs:.3f} lbs")

            print(f"***  Required Hold Down Force: {hd_force_lbs:.3f} lbs")
            print(
                f"***  Required Wall Anchorage Unit Shear: {basic_unit_shear_plf:.3f} plf"
            )
            print(
                f"***  Average of 4-Term Deflections = {sum(pier_deflections_four_term)/len(pier_deflections_four_term):.3f} in"
            )
            print(f"***  % Drift  = (Cd * Delta) / (Hwall * 12): {percent_drift:.4f} %")
            print(f"***  Drift Ratio = (Hwall * 12) / (Cd * Delta)  = H/{delta_h_over:.1f}")
            print("***")
            print("*" * tick_count)

            # SVG Generation
            svg_x = 1024
            svg_y = 768
            panel_color = "darkkhaki"
            svg_string = [f'<svg xmlns="http://www.w3.org/2000/svg" id="svgPrimary" width="{svg_x}" height="{svg_y}">']
            # Transformation matrix for svg to reorient axis and scale to fit
            svg_string.append('<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" /></marker></defs>')
            
            svg_dx = Lwall_ft + 3
            svg_dy = Hwall_ft + 4

            scalex = (svg_x - 20)/svg_dx
            scaley = (svg_y - 20)/svg_dy
            svg_scale = min(scalex,scaley)

            svg_tx = 10
            svg_ty = 10 + (svg_dy*svg_scale)
            
            tmatrix = f'<g id="svgViewport" transform="matrix({svg_scale},0,0,{-1*svg_scale},{svg_tx},{svg_ty})">'

            svg_string.append(tmatrix)
            # Applied Load
            svg_string.append(f'<line x1="0" y1="{Hwall_ft+2}" x2="2.9" y2="{Hwall_ft+2}" stroke="black" stroke-width="{3/64}" marker-end="url(#arrow)" />')
            svg_string.append(f'<text x="0" y="{-1*(Hwall_ft+2+(3/16))}" fill="blue" dominant-baseline="central" text-anchor="start" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> V: {V_lbs:.1f} lbs </text>')
            svg_string.append(f'<text x="0" y="{-1*(Hwall_ft+2-(3/8))}" fill="blue" dominant-baseline="central" text-anchor="start" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> V,delta: {Vdelta_lbs:.1f} lbs </text>')

            if endchord_above_lbs != 0:
                svg_string.append(f'<line x1="3" y1="{Hwall_ft+2}" x2="3" y2="{Hwall_ft+4}" stroke="black" stroke-width="{3/64}" marker-end="url(#arrow)" />')
                svg_string.append(f'<text x="3.25" y="{-1*(Hwall_ft+4-(3/16))}" fill="blue" dominant-baseline="central" text-anchor="start" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> HD,above: {endchord_above_lbs:.1f} lbs </text>')
                svg_string.append(f'<line x1="{Lwall_ft+3}" y1="{Hwall_ft+2+(3/16)}" x2="{Lwall_ft+3}" y2="{Hwall_ft+4}" stroke="black" stroke-width="{3/64}" marker-start="url(#arrow)" />')
                svg_string.append(f'<text x="{Lwall_ft+2.75}" y="{-1*(Hwall_ft+4-(3/16))}" fill="blue" dominant-baseline="central" text-anchor="end" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> HD,above: {endchord_above_lbs:.1f} lbs </text>')
            
            svg_string.append(f'<line x1="3" y1="{0}" x2="3" y2="{2}" stroke="black" stroke-width="{3/64}" marker-start="url(#arrow)" />')
            svg_string.append(f'<text x="3.25" y="{-1*(3/16)}" fill="blue" dominant-baseline="central" text-anchor="start" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> HD: {hd_force_lbs:.1f} lbs </text>')
            svg_string.append(f'<line x1="{Lwall_ft+3}" y1="{-(3/16)}" x2="{Lwall_ft+3}" y2="{2-(3/16)}" stroke="black" stroke-width="{3/64}" marker-end="url(#arrow)" />')
            svg_string.append(f'<text x="{Lwall_ft+2.75}" y="{-1*(3/16)}" fill="blue" dominant-baseline="central" text-anchor="end" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> HD: {hd_force_lbs:.1f} lbs </text>')
            
            svg_string.append(f'<line x1="{(Lwall_ft/2) + 3 - (Lwall_ft/6)}" y1="{2-(3/8)}" x2="{(Lwall_ft/2) + 3 + (Lwall_ft/6)}" y2="{2-(3/8)}" stroke="black" stroke-width="{3/64}" marker-start="url(#arrow)" />')
            svg_string.append(f'<text x="{Lwall_ft/2 + 3}" y="{-1*(2-(3/8)-(5/16))}" fill="blue" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> Required Wall Anchorage Unit Shear: {basic_unit_shear_plf:.3f} plf </text>')
            svg_string.append(f'<text x="{Lwall_ft/2 + 3}" y="{-1*(2-(6/8)-(7/16))}" fill="blue" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> Average of 4-Term Deflections = {sum(pier_deflections_four_term)/len(pier_deflections_four_term):.3f} in  - H/{delta_h_over:.1f} or {percent_drift:.4f}%</text>')

            # Piers
            for i,j in enumerate(piers):
                # pier x
                if i == 0:
                    px = 0 + 3
                else:
                    px = sum(piers[:i])+sum(openings[:i]) + 3

                text_x = px+(j/2)
                text_y = hb_ft + (ho_ft/2)
                svg_string.append(f'<rect width="{j}" height="{Hwall_ft}" x="{px}" y="2" fill="{panel_color}" stroke="black" stroke-width="{3/64}"/>')
                svg_string.append(f'<line x1="{px}" y1="{hb_ft + 2}" x2="{j+px}" y2="{hb_ft + 2}" stroke="black" stroke-width="{3/64}" stroke-dasharray="0.125,0.25" />')
                svg_string.append(f'<line x1="{px}" y1="{hb_ft+ho_ft + 2}" x2="{j+px}" y2="{hb_ft+ho_ft + 2}" stroke="black" stroke-width="{3/64}" stroke-dasharray="0.125,0.25" />')
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2+(3/8))}" fill="black" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> Analysis: {pier_shears_plf[i]:.1f} plf </text>')
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="black" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> Method 1: {pier_shears_plf[i]/method1_af[i]:.1f} plf </text>')
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2-(3/8))}" fill="black" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> Method 2: {pier_shears_plf[i]/method2_af[i]:.1f} plf </text>')
                text_y = hb_ft/2
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="black" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {corner_unit_shears_plf[i]:.1f} plf </text>')
                text_y = hb_ft + ho_ft + (ha_ft/2)
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="black" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {corner_unit_shears_plf[i]:.1f} plf </text>')
            # Openings
            for i,j in enumerate(openings):

                ox = sum(piers[:i]) + piers[i] + sum(openings[:i])+3

                # Bottom Panel
                svg_string.append(f'<rect width="{j}" height="{hb_ft}" x="{ox}" y="2" fill="{panel_color}" stroke="black" stroke-width="{3/64}"/>')
                # Top Panel
                svg_string.append(f'<rect width="{j}" height="{ha_ft}" x="{ox}" y="{hb_ft+ho_ft+2}" fill="{panel_color}" stroke="black" stroke-width="{3/64}"/>')
                
                text_x = ox + (j/2)
                text_y = hb_ft/2
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="black" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {opening_shears_plf[i]:.1f} plf </text>')
                text_y = hb_ft + ho_ft + (ha_ft/2)
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="black" dominant-baseline="central" text-anchor="middle" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {opening_shears_plf[i]:.1f} plf </text>')

                force_left_text = corner_forces_lbs[i][0]
                force_right_text = corner_forces_lbs[i][1]
                text_x = ox - 0.125
                text_y = hb_ft + (3/16)
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="blue" dominant-baseline="central" text-anchor="end" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {force_left_text:.1f} lbs </text>')
                text_x = ox - 0.125
                text_y = hb_ft + ho_ft - (3/16)
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="blue" dominant-baseline="central" text-anchor="end" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {force_left_text:.1f} lbs </text>')
                text_x = ox + j + 0.125
                text_y = hb_ft + (3/16)
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="blue" dominant-baseline="central" text-anchor="start" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {force_right_text:.1f} lbs </text>')
                text_x = ox + j + 0.125
                text_y = hb_ft + ho_ft - (3/16)
                svg_string.append(f'<text x="{text_x}" y="{-1*(text_y+2)}" fill="blue" dominant-baseline="central" text-anchor="start" font-size="{3/8}" font-weight="bold" transform="scale(1,-1)"> {force_right_text:.1f} lbs </text>')
            
            svg_string.append("</g>")
            svg_string.append("</svg>")

            svg_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"ftao.svg"), "w")
            for i in svg_string:
                svg_file.write(i+"\n")

            svg_file.close()

            
        else:
            print("----BEGIN ERRORS-----")
            for error in errors:
                print(error)
            print("----END ERRORS-----")

    else:
        print("----BEGIN ERRORS-----")
        for error in errors:
            print(error)
        print("----END ERRORS-----")
