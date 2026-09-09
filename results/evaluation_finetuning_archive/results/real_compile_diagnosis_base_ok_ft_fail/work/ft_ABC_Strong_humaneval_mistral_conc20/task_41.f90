program car_race_collision_demo
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Compute result
  result = car_race_collision(n)

  ! Output result
  print(*,*) result

contains

  integer function car_race_collision(n)
    integer, intent(in) :: n
    car_race_collision = n * n
  end function car_race_collision

end program car_race_collision_demo