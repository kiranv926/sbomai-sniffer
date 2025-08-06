package com.sbomai.core.repository;

import com.sbomai.core.domain.Scan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.UUID;

@Repository
public interface ScanRepository extends JpaRepository<Scan, UUID> {
    // Custom query methods can be added here
}
