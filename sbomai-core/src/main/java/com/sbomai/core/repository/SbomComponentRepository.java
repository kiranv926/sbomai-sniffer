package com.sbomai.core.repository;

import com.sbomai.core.domain.SbomComponent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.UUID;
import java.util.List;

@Repository
public interface SbomComponentRepository extends JpaRepository<SbomComponent, UUID> {
    List<SbomComponent> findBySbomId(UUID sbomId);
}
