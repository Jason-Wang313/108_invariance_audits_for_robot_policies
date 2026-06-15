# Literature Map

Paper: 108 invariance_audits_for_robot_policies

Field box: equivariant robot learning, domain randomization, invariance learning, and policy safety auditing.

Thesis: physically valid invariances should be retained, while physically invalid invariances should be rejected.

## Crowded Neighbor Clusters

- Group equivariant networks and equivariant robot manipulation.
- Transporter-style manipulation and action-space equivariance.
- Domain randomization and sim-to-real robustness.
- Invariant risk minimization and contrastive invariance learning.
- Conformal or uncertainty-based shift filters.

## Hidden Assumptions Attacked

- Data augmentation always encodes safe invariances.
- Equivariance is safe whenever the scene transform is geometric.
- Domain randomization cannot erase necessary physical distinctions.
- Distribution-shift filters can replace physical-validity tests.
- A policy can treat contact-frame, affordance, and temporal-order changes as nuisance variation.

## Boundary

The project centers a mechanism-level change: audit invariances for physical validity before deployment, preserving valid perceptual/geometric invariances while rejecting invalid contact, material, affordance, and temporal transformations.
