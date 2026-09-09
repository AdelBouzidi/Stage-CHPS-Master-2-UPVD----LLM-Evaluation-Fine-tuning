program car_race_collision
  implicit none
  integer :: n, collisions

  ! Read input
  read(*,*) n

  ! Calculate collisions
  collisions = n * n

  ! Output result
  print *, collisions

end program car_race_collision