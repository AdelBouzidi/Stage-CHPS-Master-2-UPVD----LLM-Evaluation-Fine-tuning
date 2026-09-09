program prime_check
  implicit none
  integer :: n
  logical :: result

  read(*,*) n
  result = is_prime(n)
  print *, result
contains
  logical function is_prime(num)
    integer, intent(in) :: num
    integer :: i
    if (num <= 1) then
      result = .false.
    else if (num == 2) then
      result = .true.
    else if (mod(num, 2) == 0) then
      result = .false.
    else
      result = .true.
      do i = 3, int(sqrt(real(num))), 2
        if (mod(num, i) == 0) then
          result = .false.
          exit
        end if
      end do
    end if
  end function is_prime
end program prime_check